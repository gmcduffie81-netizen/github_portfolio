from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Literal

TicketStatus = Literal[
    "Open",
    "In Progress",
    "Scheduled",
    "Awaiting HQ",
    "Closed",
]
ScheduleStatus = Literal["Scheduled", "Completed", "Cancelled"]


@dataclass
class Note:
    at: str
    who: str
    text: str


@dataclass
class MaintTicket:
    ticket_id: int
    van_tag: str
    office: str
    status: TicketStatus = "Open"
    schedule_date: date | None = None
    schedule_status: ScheduleStatus | None = None
    vendor: str | None = None
    notes: list[Note] = field(default_factory=list)

    def add_note(self, who: str, text: str) -> None:
        self.notes.append(
            Note(at=datetime.now().strftime("%Y-%m-%d %H:%M"), who=who, text=text)
        )

    def schedule(self, when: date, vendor: str, who: str) -> None:
        self.schedule_date = when
        self.vendor = vendor
        self.schedule_status = "Scheduled"
        self.status = "Scheduled"
        self.add_note(who, f"Scheduled {when.isoformat()} at {vendor}")

    def mark_complete(self, who: str) -> None:
        self.status = "Closed"
        if self.schedule_status == "Scheduled":
            self.schedule_status = "Completed"
        self.add_note(who, "Closed complete")

    def mark_missed(self, who: str) -> None:
        missed = self.schedule_date.isoformat() if self.schedule_date else "unknown"
        self.status = "Open"
        if self.schedule_status == "Scheduled":
            self.schedule_status = "Cancelled"
        self.schedule_date = None
        self.vendor = None
        self.add_note(who, f"Missed appointment {missed}; set Open")

    def is_overdue(self, today: date | None = None) -> bool:
        today = today or date.today()
        if self.status == "Closed":
            return False
        if not self.schedule_date or self.schedule_status != "Scheduled":
            return False
        return self.schedule_date < today
