from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

ClaimStatus = Literal[
    "Open",
    "Contact Attempted",
    "Assessment Scheduled",
    "Under Review",
    "Accepted",
    "Denied",
    "No Contact",
    "Closed",
]


@dataclass
class ClaimEvent:
    at: str
    who: str
    action: str
    detail: str = ""


@dataclass
class DamageClaim:
    claim_id: str
    customer_name: str
    office: str
    status: ClaimStatus = "Open"
    events: list[ClaimEvent] = field(default_factory=list)
    in_house_repair_cost: float | None = None
    contractor_quote: float | None = None

    def _log(self, who: str, action: str, detail: str = "") -> None:
        self.events.append(
            ClaimEvent(
                at=datetime.now().strftime("%Y-%m-%d %H:%M"),
                who=who,
                action=action,
                detail=detail,
            )
        )

    def log_contact(self, who: str, note: str) -> None:
        self.status = "Contact Attempted"
        self._log(who, "contact", note)

    def schedule_assessment(self, who: str, how: str) -> None:
        self.status = "Assessment Scheduled"
        self._log(who, "assessment", how)

    def accept_liability(self, who: str, reason: str) -> None:
        self.status = "Accepted"
        self._log(who, "accept", reason)

    def deny_claim(self, who: str, reason: str) -> None:
        self.status = "Denied"
        self._log(who, "deny", reason)

    def record_contractor_quote(self, who: str, amount: float) -> None:
        self.contractor_quote = amount
        self._log(who, "contractor_quote", f"{amount:.2f}")

    def complete_in_house_repair(self, who: str, amount: float, work: str) -> None:
        self.in_house_repair_cost = amount
        self.status = "Closed"
        self._log(who, "in_house_repair", f"{amount:.2f} | {work}")

    def savings_vs_contractor(self) -> float | None:
        if self.contractor_quote is None or self.in_house_repair_cost is None:
            return None
        return round(self.contractor_quote - self.in_house_repair_cost, 2)
