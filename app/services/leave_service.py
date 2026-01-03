from app.models.leave import LeaveRequest


def apply_leave(session, employee_id, data):
    leave = LeaveRequest(
        employee_id=employee_id,
        leave_type=data.leave_type,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status="PENDING"   # 👈 force default
    )
    session.add(leave)
    session.commit()
    session.refresh(leave)
    return leave


def update_leave_status(session, leave_id, admin_id, status: str):
    leave = session.get(LeaveRequest, leave_id)

    if not leave:
        raise Exception("Leave request not found")

    # 🔒 prevent re-approval / re-rejection
    if leave.status != "PENDING":
        raise Exception("Leave already processed")

    leave.status = status
    leave.reviewed_by = admin_id

    session.commit()
    session.refresh(leave)
    return leave
