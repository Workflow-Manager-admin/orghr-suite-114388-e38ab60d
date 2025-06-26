from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

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
