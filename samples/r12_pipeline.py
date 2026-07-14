from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any, Iterable


@dataclass
class ReasonDictionary:
    rows: list[dict[str, str]]

    @classmethod
    def from_rows(cls, rows: Iterable[dict[str, str]]) -> "ReasonDictionary":
        cleaned = []
        for r in rows:
            code = str(r.get("code") or r.get("Keyword") or "").strip()
            label = str(r.get("label") or r.get("Replacement") or "").strip()
            if code and label:
                cleaned.append({"code": code, "label": label})
        cleaned.sort(key=lambda x: len(x["code"]), reverse=True)
        return cls(rows=cleaned)

    def classify(self, note_text: str) -> str:
        text = note_text or ""
        if not text or text.upper() == "N/A":
            return "Unclassified"
        for row in self.rows:
            if re.search(re.escape(row["code"]), text, re.IGNORECASE):
                return row["label"]
        lowered = text.lower()
        if "weather" in lowered or "storm" in lowered:
            return "Weather related (heuristic)"
        if "no signal" in lowered or "signal loss" in lowered:
            return "Signal loss (heuristic)"
        return "Unclassified"


@dataclass
class TroubleCall:
    work_order: str
    account: str
    office: str
    region: str
    create_date: date
    schedule_date: date | None
    assigned_tech: str | None
    prior_work_order: str | None
    prior_tech: str | None
    prior_notes: str
    reason_label: str = ""
    is_return: bool = False


@dataclass
class DailyR12Pack:
    as_of: date
    new_creates_yesterday: list[TroubleCall] = field(default_factory=list)
    scheduled_today: list[TroubleCall] = field(default_factory=list)
    returns_completed_yesterday: list[TroubleCall] = field(default_factory=list)

    def summary(self) -> dict[str, int]:
        return {
            "new_creates_yesterday": len(self.new_creates_yesterday),
            "scheduled_today": len(self.scheduled_today),
            "returns_completed_yesterday": len(self.returns_completed_yesterday),
        }


NOISE_OPERATOR_IDS = {"288", "SYSTEM", "BOT"}


def filter_notes(raw_rows: list[dict[str, str]], create_day: date) -> str:
    kept: list[str] = []
    for row in raw_rows:
        op = str(row.get("operator_id") or "").strip()
        if op in NOISE_OPERATOR_IDS:
            continue
        note = str(row.get("text") or "").strip()
        if not note:
            continue
        d = row.get("note_date")
        if isinstance(d, date) and d != create_day:
            continue
        kept.append(note)
    return " | ".join(kept) if kept else "N/A"


def build_daily_pack(
    rows: list[TroubleCall],
    dictionary: ReasonDictionary,
    today: date | None = None,
) -> DailyR12Pack:
    today = today or date.today()
    yesterday = today - timedelta(days=1)
    pack = DailyR12Pack(as_of=today)
    for tc in rows:
        tc.reason_label = dictionary.classify(tc.prior_notes)
        if tc.create_date == yesterday:
            pack.new_creates_yesterday.append(tc)
        if tc.schedule_date == today and tc.assigned_tech:
            pack.scheduled_today.append(tc)
        if tc.is_return and tc.create_date == yesterday:
            pack.returns_completed_yesterday.append(tc)
    return pack


def row_for_export(tc: TroubleCall) -> dict[str, Any]:
    return {
        "work_order": tc.work_order,
        "account": tc.account,
        "office": tc.office,
        "region": tc.region,
        "create_date": tc.create_date.isoformat(),
        "schedule_date": tc.schedule_date.isoformat() if tc.schedule_date else None,
        "assigned_tech": tc.assigned_tech,
        "prior_work_order": tc.prior_work_order,
        "prior_tech": tc.prior_tech,
        "reason": tc.reason_label,
        "prior_notes": tc.prior_notes,
        "is_return": tc.is_return,
    }


def pack_to_sections(pack: DailyR12Pack) -> dict[str, Any]:
    return {
        "as_of": pack.as_of.isoformat(),
        "counts": pack.summary(),
        "new_creates_yesterday": [row_for_export(t) for t in pack.new_creates_yesterday],
        "scheduled_today": [row_for_export(t) for t in pack.scheduled_today],
        "returns_completed_yesterday": [
            row_for_export(t) for t in pack.returns_completed_yesterday
        ],
    }


def scrape_shape_example() -> list[str]:
    return [
        "login_vendor_ops",
        "open_tc12_scorecard_report",
        "export_or_page_rows_since_watermark",
        "for_each_prior_wo: open_details + account_notes",
        "drop_noise_operators",
        "dictionary_classify",
        "write_csv_and_publish_internal_host",
    ]
