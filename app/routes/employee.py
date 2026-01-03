from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.leave import LeaveCreate

from app.services.leave_service import apply_leave
from app.services.payroll_service import get_my_payroll

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)

# -----------------------------
# PROFILE
# -----------------------------
@router.get("/me")
def my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# -----------------------------
# LEAVE
# -----------------------------
@router.post("/leave/apply")
def apply_leave_route(
    data: LeaveCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return apply_leave(session, current_user.id, data)


# -----------------------------
# PAYROLL
# -----------------------------
@router.get("/payroll")
def view_my_payroll(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return get_my_payroll(session, current_user.id)
