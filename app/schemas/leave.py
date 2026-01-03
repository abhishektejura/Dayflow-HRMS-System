from sqlmodel import SQLModel
from datetime import date


class LeaveCreate(SQLModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: str
