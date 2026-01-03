from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token
)
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# -----------------------------
# SCHEMAS (LOCAL – SIMPLE)
# -----------------------------
class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str = "EMPLOYEE"


# -----------------------------
# REGISTER
# -----------------------------
@router.post("/register")
def register(
    data: RegisterRequest,
    session: Session = Depends(get_session)
):
    existing_user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=data.email,
        password_hash=get_password_hash(data.password),
        role=data.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }


# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login")
def login(
    data: LoginRequest,
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
