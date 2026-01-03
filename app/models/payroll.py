from sqlmodel import SQLModel, Field
from typing import Optional

class Payroll(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int
    base_salary: float
    present_days: int
    leave_days: int
    net_salary: float
