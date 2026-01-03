from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Attendance(SQLModel, table=True):
    __tablename__ = "attendance"

    id: Optional[int] = Field(default=None, primary_key=True)

    employee_id: int = Field(index=True)

    attendance_date: date = Field(index=True)

    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None

    status: str = Field(nullable=False)  # PRESENT | HALF_DAY | ABSENT
