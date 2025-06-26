from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from .models import Employee, EmployeeCreate, EmployeeUpdate, EmployeeOut, Department, DepartmentOut, Role, RoleOut
from .db import db_employees, db_departments, db_roles, create_employee, update_employee, delete_employee
from .auth import get_current_active_user

router = APIRouter()

# ---------------- Employee Endpoints --------------------
@router.get("/employees", response_model=List[EmployeeOut], tags=["Employees"], summary="List all employees")
def list_employees():
    """List all employees."""
    return [
        EmployeeOut(**emp.dict(), department=db_departments.get(emp.department_id), role=db_roles.get(emp.role_id))
        for emp in db_employees.values()
    ]

@router.get("/employees/{employee_id}", response_model=EmployeeOut, tags=["Employees"], summary="Get employee details")
def get_employee(employee_id: int):
    """Get employee details by ID."""
    emp = db_employees.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeOut(**emp.dict(), department=db_departments.get(emp.department_id), role=db_roles.get(emp.role_id))

@router.post("/employees", response_model=EmployeeOut, status_code=201, tags=["Employees"], summary="Create employee")
def create_new_employee(employee: EmployeeCreate):
    """Create a new employee record."""
    emp = create_employee(employee)
    return EmployeeOut(**emp.dict(), department=db_departments.get(emp.department_id), role=db_roles.get(emp.role_id))

@router.put("/employees/{employee_id}", response_model=EmployeeOut, tags=["Employees"], summary="Update employee")
def update_employee_endpoint(employee_id: int, employee: EmployeeUpdate):
    """Update employee information."""
    updated = update_employee(employee_id, employee)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeOut(**updated.dict(), department=db_departments.get(updated.department_id), role=db_roles.get(updated.role_id))

@router.delete("/employees/{employee_id}", status_code=204, tags=["Employees"], summary="Delete employee")
def delete_employee_endpoint(employee_id: int):
    """Delete an employee by ID."""
    success = delete_employee(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return

# ---------------- Department Endpoints --------------------
@router.get("/departments", response_model=List[DepartmentOut], tags=["Departments"], summary="List all departments")
def list_departments():
    """List all departments."""
    return list(db_departments.values())

@router.post("/departments", response_model=DepartmentOut, status_code=201, tags=["Departments"], summary="Create a department")
def create_department(department: Department):
    """Create a new department."""
    if department.id in db_departments:
        raise HTTPException(status_code=400, detail="Department ID already exists")
    db_departments[department.id] = department
    return department

# ---------------- Role Endpoints --------------------
@router.get("/roles", response_model=List[RoleOut], tags=["Roles"], summary="List all roles")
def list_roles():
    """List all roles."""
    return list(db_roles.values())

@router.post("/roles", response_model=RoleOut, status_code=201, tags=["Roles"], summary="Create a role")
def create_role(role: Role):
    """Create a new role."""
    if role.id in db_roles:
        raise HTTPException(status_code=400, detail="Role ID already exists")
    db_roles[role.id] = role
    return role
