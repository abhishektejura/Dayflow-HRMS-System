from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class LeaveRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str = "PENDING"
    reviewed_by: Optional[int] = None
