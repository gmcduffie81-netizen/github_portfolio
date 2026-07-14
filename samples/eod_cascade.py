from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import Callable


class CascadeStage(str, Enum):
    PULL_EXTERNAL = "pull_external"
    OFFICE_SUPERVISOR = "office_supervisor"
    WAIT_FOR_NOTES = "wait_for_notes"
    RESYNC_NOTES = "resync_notes"
    REGIONAL_MANAGER = "regional_manager"
    COMPANY_FINAL = "company_final"


@dataclass
class OfficeContact:
    office: str
    region: str
    supervisor_email: str
    afs_email: str | None = None


@dataclass
class RegionContact:
    region: str
    manager_email: str
    manager_name: str


@dataclass
class JobRow:
    work_order: str
    office: str
    region: str
    tech: str
    incomplete: bool
    external_notes: str = ""
    supervisor_notes: str = ""
    regional_notes: str = ""


@dataclass
class CascadeConfig:
    report_date: date
    office_contacts: list[OfficeContact]
    region_contacts: list[RegionContact]
    company_emails: list[str]
    supervisor_send_at: time = time(5, 0)
    note_window_hours: int = 4
    regional_send_at: time = time(9, 0)
    company_send_at: time = time(11, 0)


@dataclass
class OutboundMail:
    stage: CascadeStage
    to: list[str]
    subject: str
    body_summary: str
    work_orders: list[str] = field(default_factory=list)


def report_date_for_run(now: datetime | None = None) -> date:
    now = now or datetime.now()
    if now.weekday() == 6:
        raise RuntimeError("skip_sunday")
    days = 2 if now.weekday() == 0 else 1
    return (now - timedelta(days=days)).date()


def jobs_for_office(jobs: list[JobRow], office: str) -> list[JobRow]:
    return [j for j in jobs if j.office.lower() == office.lower()]


def jobs_for_region(jobs: list[JobRow], region: str) -> list[JobRow]:
    return [j for j in jobs if j.region.lower() == region.lower()]


def needing_supervisor_notes(jobs: list[JobRow]) -> list[JobRow]:
    return [j for j in jobs if j.incomplete and not (j.supervisor_notes or "").strip()]


def apply_supervisor_updates(
    jobs: list[JobRow], updates: dict[str, str]
) -> list[JobRow]:
    out = []
    for j in jobs:
        note = updates.get(j.work_order)
        if note:
            j = JobRow(**{**j.__dict__, "supervisor_notes": note})
        out.append(j)
    return out


def build_supervisor_wave(
    cfg: CascadeConfig, jobs: list[JobRow]
) -> list[OutboundMail]:
    mail: list[OutboundMail] = []
    for oc in cfg.office_contacts:
        office_jobs = jobs_for_office(jobs, oc.office)
        if not office_jobs:
            continue
        need = needing_supervisor_notes(office_jobs)
        mail.append(
            OutboundMail(
                stage=CascadeStage.OFFICE_SUPERVISOR,
                to=[oc.supervisor_email]
                + ([oc.afs_email] if oc.afs_email else []),
                subject=f"Office notes needed · {oc.office} · {cfg.report_date}",
                body_summary=(
                    f"{len(office_jobs)} jobs · {len(need)} still need supervisor notes"
                ),
                work_orders=[j.work_order for j in office_jobs],
            )
        )
    return mail


def build_regional_wave(
    cfg: CascadeConfig, jobs: list[JobRow]
) -> list[OutboundMail]:
    mail: list[OutboundMail] = []
    for rc in cfg.region_contacts:
        region_jobs = jobs_for_region(jobs, rc.region)
        if not region_jobs:
            continue
        with_notes = sum(1 for j in region_jobs if j.supervisor_notes)
        mail.append(
            OutboundMail(
                stage=CascadeStage.REGIONAL_MANAGER,
                to=[rc.manager_email],
                subject=f"Regional review · {rc.region} · {cfg.report_date}",
                body_summary=(
                    f"{len(region_jobs)} jobs · {with_notes} with supervisor notes"
                ),
                work_orders=[j.work_order for j in region_jobs],
            )
        )
    return mail


def build_company_final(
    cfg: CascadeConfig, jobs: list[JobRow]
) -> OutboundMail:
    incomplete = [j for j in jobs if j.incomplete]
    return OutboundMail(
        stage=CascadeStage.COMPANY_FINAL,
        to=list(cfg.company_emails),
        subject=f"Company final · day prior {cfg.report_date}",
        body_summary=(
            f"{len(jobs)} total · {len(incomplete)} incomplete/reschedule focus"
        ),
        work_orders=[j.work_order for j in incomplete],
    )


def run_cascade(
    cfg: CascadeConfig,
    pull_jobs: Callable[[date], list[JobRow]],
    resync_jobs: Callable[[date], list[JobRow]],
    queue_mail: Callable[[OutboundMail], None],
) -> dict[str, int]:
    jobs = pull_jobs(cfg.report_date)
    for m in build_supervisor_wave(cfg, jobs):
        queue_mail(m)
    jobs = resync_jobs(cfg.report_date)
    for m in build_regional_wave(cfg, jobs):
        queue_mail(m)
    final = build_company_final(cfg, jobs)
    queue_mail(final)
    return {
        "jobs": len(jobs),
        "supervisor_mails": len(cfg.office_contacts),
        "regional_mails": len(cfg.region_contacts),
        "company_mails": 1,
    }


CASCADE_ORDER = [
    CascadeStage.PULL_EXTERNAL,
    CascadeStage.OFFICE_SUPERVISOR,
    CascadeStage.WAIT_FOR_NOTES,
    CascadeStage.RESYNC_NOTES,
    CascadeStage.REGIONAL_MANAGER,
    CascadeStage.COMPANY_FINAL,
]
