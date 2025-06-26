from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

# --- SQLAlchemy ORM imports for helpers ---
from .db import DepartmentORM, RoleORM, EmployeeORM

# PUBLIC_INTERFACE
class Department(BaseModel):
    """Department model."""
    id: int = Field(..., description="Unique identifier for the department")
    name: str = Field(..., description="Department name")
    description: Optional[str] = Field(None, description="Description of the department")

# PUBLIC_INTERFACE
class Role(BaseModel):
    """Role model."""
    id: int = Field(..., description="Unique identifier for the role")
    name: str = Field(..., description="Role name")
    description: Optional[str] = Field(None, description="Description of the role")

# PUBLIC_INTERFACE
class EmployeeBase(BaseModel):
    """Base model for employee."""
    first_name: str = Field(..., description="Employee first name")
    last_name: str = Field(..., description="Employee last name")
    email: str = Field(..., description="Employee email address")
    is_active: bool = Field(True, description="Whether the employee is active")
    department_id: int = Field(..., description="Department ID")
    role_id: int = Field(..., description="Role ID")

# PUBLIC_INTERFACE
class EmployeeCreate(EmployeeBase):
    """Model for creating employee. Password required."""
    password: str = Field(..., description="Password for employee login")

# PUBLIC_INTERFACE
class EmployeeUpdate(BaseModel):
    """Model for updating employee."""
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
    department_id: Optional[int]
    role_id: Optional[int]

# PUBLIC_INTERFACE
class Employee(EmployeeBase):
    """Employee model, including ID."""
    id: int = Field(..., description="Employee ID")
    created_at: Optional[datetime] = None

# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """Login model."""
    email: str = Field(..., description="User email")
    password: str = Field(..., description="Password")

# PUBLIC_INTERFACE
class Token(BaseModel):
    """JWT Token response."""
    access_token: str
    token_type: str = "bearer"

# PUBLIC_INTERFACE
class TokenData(BaseModel):
    """Data in a JWT token."""
    user_id: Optional[int] = None

# PUBLIC_INTERFACE
class RoleOut(Role):
    pass

# PUBLIC_INTERFACE
class DepartmentOut(Department):
    pass

# PUBLIC_INTERFACE
class EmployeeOut(Employee):
    department: Optional[DepartmentOut]
    role: Optional[RoleOut]

# --- ORM --> Pydantic utilities ---

def department_orm_to_pydantic(orm: DepartmentORM) -> DepartmentOut:
    return DepartmentOut(id=orm.id, name=orm.name, description=orm.description)

def role_orm_to_pydantic(orm: RoleORM) -> RoleOut:
    return RoleOut(id=orm.id, name=orm.name, description=orm.description)

def employee_orm_to_pydantic(emp: EmployeeORM, dep: DepartmentORM = None, role: RoleORM = None) -> EmployeeOut:
    """Convert SQLAlchemy employee + relations to pydantic EmployeeOut."""
    return EmployeeOut(
        id=emp.id,
        first_name=emp.first_name,
        last_name=emp.last_name,
        email=emp.email,
        is_active=emp.is_active,
        department_id=emp.department_id,
        role_id=emp.role_id,
        created_at=emp.created_at,
        department=department_orm_to_pydantic(dep) if dep else None,
        role=role_orm_to_pydantic(role) if role else None,
    )
