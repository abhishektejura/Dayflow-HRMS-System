from datetime import date, datetime
from sqlmodel import Session, select

from app.models.attendance import Attendance


# -----------------------------
# CHECK-IN (Employee)
# -----------------------------
def check_in(session: Session, employee_id: int):
    today = date.today()

    existing = session.exec(
        select(Attendance)
        .where(Attendance.employee_id == employee_id)
        .where(Attendance.date == today)
    ).first()

    if existing:
        raise Exception("Already checked in for today")

    attendance = Attendance(
        employee_id=employee_id,
        date=today,
        check_in=datetime.utcnow(),
        status="PRESENT"
    )

    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return attendance


# -----------------------------
# CHECK-OUT (Employee)
# -----------------------------
def check_out(session: Session, employee_id: int):
    today = date.today()

    record = session.exec(
        select(Attendance)
        .where(Attendance.employee_id == employee_id)
        .where(Attendance.date == today)
    ).first()

    if not record:
        raise Exception("No check-in found for today")

    if record.check_out:
        raise Exception("Already checked out")

    record.check_out = datetime.utcnow()

    worked_seconds = (record.check_out - record.check_in).seconds
    worked_hours = worked_seconds / 3600

    record.status = "HALF_DAY" if worked_hours < 4 else "PRESENT"

    session.commit()
    session.refresh(record)
    return record


# -----------------------------
# VIEW OWN ATTENDANCE
# -----------------------------
def get_my_attendance(session: Session, employee_id: int):
    return session.exec(
        select(Attendance)
        .where(Attendance.employee_id == employee_id)
        .order_by(Attendance.date.desc())
    ).all()


# -----------------------------
# ADMIN: VIEW ALL ATTENDANCE
# -----------------------------
def get_all_attendance(session: Session):
    return session.exec(
        select(Attendance)
        .order_by(Attendance.date.desc())
    ).all()
