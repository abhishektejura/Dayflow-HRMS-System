from sqlmodel import SQLModel
from app.db.session import engine

# Import ALL models here (important!)
from app.models.user import User
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.leave import LeaveRequest
from app.models.payroll import Payroll


def init_db():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully")
