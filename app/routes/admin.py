from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.deps import get_current_admin
from app.db.session import get_session
from app.services.leave_service import update_leave_status
from app.models.leave import LeaveRequest

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# -----------------------------
# VIEW ALL LEAVE REQUESTS
# -----------------------------
@router.get("/leaves")
def get_all_leaves(
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin)
):
    return session.exec(select(LeaveRequest)).all()


# -----------------------------
# APPROVE LEAVE
# -----------------------------
@router.post("/leave/{leave_id}/approve")
def approve_leave(
    leave_id: int,
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin)
):
    return update_leave_status(
        session=session,
        leave_id=leave_id,
        admin_id=admin.id,
        status="APPROVED"
    )


# -----------------------------
# REJECT LEAVE
# -----------------------------
@router.post("/leave/{leave_id}/reject")
def reject_leave(
    leave_id: int,
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin)
):
    return update_leave_status(
        session=session,
        leave_id=leave_id,
        admin_id=admin.id,
        status="REJECTED"
    )
