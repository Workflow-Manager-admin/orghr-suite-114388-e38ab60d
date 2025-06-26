from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth_endpoints import router as auth_router
from .routes import router as core_router

openapi_tags = [
    {"name": "Employees", "description": "Employee CRUD operations"},
    {"name": "Roles", "description": "Role management"},
    {"name": "Departments", "description": "Department management"},
    {"name": "Authentication", "description": "Login, logout, and user management"},
]

app = FastAPI(
    title="Employee Management API",
    description="RESTful API for Employee Record, Authentication, Role, and Department Management",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(core_router)

@app.get("/", tags=["Health"])
def health_check():
    """Health check for service."""
    return {"message": "Healthy"}
