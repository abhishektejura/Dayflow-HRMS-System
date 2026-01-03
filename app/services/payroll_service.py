from sqlmodel import Session, select
from app.models.attendance import Attendance
from app.models.leave import LeaveRequest

DAILY_SALARY = 1000  # fixed for demo

def get_my_payroll(session: Session, employee_id: int):
    present_days = session.exec(
        select(Attendance)
        .where(Attendance.employee_id == employee_id)
        .where(Attendance.status == "PRESENT")
    ).all()

    approved_leaves = session.exec(
        select(LeaveRequest)
        .where(LeaveRequest.employee_id == employee_id)
        .where(LeaveRequest.status == "APPROVED")
    ).all()

    total_days = len(present_days) + len(approved_leaves)
    net_salary = total_days * DAILY_SALARY

    return {
        "employee_id": employee_id,
        "present_days": len(present_days),
        "approved_leave_days": len(approved_leaves),
        "daily_salary": DAILY_SALARY,
        "net_salary": net_salary
    }
