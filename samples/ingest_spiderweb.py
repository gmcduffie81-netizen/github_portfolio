from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable


class SourceKind(str, Enum):
    VENDOR_WEB_UI = "vendor_web_ui"
    INTERNAL_TICKET_HOST = "internal_ticket_host"
    TABLEAU_EXPORT = "tableau_export"
    SHAREPOINT_LIST = "sharepoint_list"
    GOOGLE_SHEET = "google_sheet"
    FORM_INTAKE = "form_intake"
    GPS_FLEET_API = "gps_fleet_api"
    FTP_DROP = "ftp_drop"


@dataclass
class SourceHit:
    kind: SourceKind
    label: str
    fetched_at: str
    raw_rows: int
    errors: list[str] = field(default_factory=list)


@dataclass
class NormalizedRow:
    source: str
    office: str | None
    tech: str | None
    work_order: str | None
    metric_name: str
    metric_value: float | None
    as_of: str
    flags: list[str] = field(default_factory=list)


def normalize_tech_name(name: str | None) -> str | None:
    if not name:
        return None
    parts = [p for p in str(name).replace(",", " ").split() if p]
    if not parts:
        return None
    return " ".join(p.capitalize() for p in parts)


def excel_serial_to_iso(serial: Any) -> str | None:
    try:
        n = int(float(serial))
        if n > 60:
            n -= 1
        from datetime import date, timedelta

        d = date(1899, 12, 30) + timedelta(days=n)
        return d.isoformat()
    except Exception:
        return None


def check_point_glitch(
    rows: list[dict[str, Any]],
    value_key: str = "points",
    expected_sum_key: str | None = "points_total",
    tolerance: float = 0.01,
) -> list[str]:
    flags: list[str] = []
    values = []
    for r in rows:
        try:
            values.append(float(r.get(value_key)))
        except Exception:
            flags.append("non_numeric_points")
    if not values:
        return flags
    s = sum(values)
    if expected_sum_key and rows and rows[0].get(expected_sum_key) is not None:
        try:
            expected = float(rows[0][expected_sum_key])
            if abs(expected - s) > tolerance:
                flags.append(f"points_sum_mismatch expected={expected} got={s}")
        except Exception:
            flags.append("points_total_unreadable")
    if any(v < 0 for v in values):
        flags.append("negative_points")
    return flags


def normalize_batch(
    source_label: str,
    raw: list[dict[str, Any]],
    metric_name: str,
    office_key: str = "office",
    tech_key: str = "tech",
    wo_key: str = "work_order",
    value_key: str = "value",
    as_of: str | None = None,
) -> list[NormalizedRow]:
    as_of = as_of or datetime.utcnow().strftime("%Y-%m-%d")
    glitch = check_point_glitch(raw, value_key=value_key)
    out: list[NormalizedRow] = []
    for r in raw:
        val = r.get(value_key)
        try:
            fval = float(val) if val is not None and val != "" else None
        except Exception:
            fval = None
            glitch = list(set(glitch + ["bad_metric_value"]))
        out.append(
            NormalizedRow(
                source=source_label,
                office=(str(r.get(office_key)).strip() if r.get(office_key) else None),
                tech=normalize_tech_name(r.get(tech_key)),
                work_order=(
                    str(r.get(wo_key)).strip() if r.get(wo_key) is not None else None
                ),
                metric_name=metric_name,
                metric_value=fval,
                as_of=as_of,
                flags=list(glitch),
            )
        )
    return out


def run_spider(
    fetchers: list[tuple[SourceKind, str, Callable[[], list[dict[str, Any]]]]],
    metric_name: str,
) -> tuple[list[SourceHit], list[NormalizedRow]]:
    hits: list[SourceHit] = []
    rows: list[NormalizedRow] = []
    stamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    for kind, label, fetch in fetchers:
        try:
            raw = fetch()
            hits.append(
                SourceHit(
                    kind=kind,
                    label=label,
                    fetched_at=stamp,
                    raw_rows=len(raw),
                )
            )
            rows.extend(normalize_batch(label, raw, metric_name=metric_name))
        except Exception as e:
            hits.append(
                SourceHit(
                    kind=kind,
                    label=label,
                    fetched_at=stamp,
                    raw_rows=0,
                    errors=[type(e).__name__],
                )
            )
    return hits, rows


SOURCE_MAP = {
    SourceKind.VENDOR_WEB_UI: "Browser automation against vendor ops / scorecards",
    SourceKind.INTERNAL_TICKET_HOST: "Internal ticket HTML host / FTP publish",
    SourceKind.TABLEAU_EXPORT: "Tableau extract or CSV drop",
    SourceKind.SHAREPOINT_LIST: "SharePoint list export",
    SourceKind.GOOGLE_SHEET: "Google Sheets API or scheduled export",
    SourceKind.FORM_INTAKE: "Form vendor webhook / poller",
    SourceKind.GPS_FLEET_API: "Fleet GPS / odometer API",
    SourceKind.FTP_DROP: "Nightly file drop",
}
