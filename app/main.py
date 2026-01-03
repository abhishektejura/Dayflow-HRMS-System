from fastapi import FastAPI

from app.routes import auth, employee, admin

app = FastAPI(
    title="Dayflow HRMS",
    description="Human Resource Management System API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Dayflow HRMS",
        "docs": "/docs",
        "auth": "/auth/*",
        "employee": "/employee/*",
        "admin": "/admin/*"
    }

# register routers
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(admin.router)
