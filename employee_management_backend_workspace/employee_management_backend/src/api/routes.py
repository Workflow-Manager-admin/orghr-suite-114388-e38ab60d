from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
import logging
from datetime import datetime
from .models import (
    Employee, EmployeeCreate, EmployeeUpdate, EmployeeOut,
    Department, DepartmentOut, Role, RoleOut,
    employee_orm_to_pydantic, department_orm_to_pydantic, role_orm_to_pydantic
)
from .db import (
    get_db, EmployeeORM, DepartmentORM, RoleORM, pwd_context
)
from .auth import get_current_active_user

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

# ---------------- Employee Endpoints --------------------
@router.get("/employees", response_model=List[EmployeeOut], tags=["Employees"], summary="List all employees")
def list_employees(db: Session = Depends(get_db)):
    """List all employees (joined with dept/role)."""
    employees = db.query(EmployeeORM).all()
    results = []
    for emp in employees:
        dep = db.query(DepartmentORM).filter_by(id=emp.department_id).first()
        role = db.query(RoleORM).filter_by(id=emp.role_id).first()
        results.append(employee_orm_to_pydantic(emp, dep, role))
    return results

@router.get("/employees/{employee_id}", response_model=EmployeeOut, tags=["Employees"], summary="Get employee details")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee details by ID."""
    emp = db.query(EmployeeORM).filter_by(id=employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    dep = db.query(DepartmentORM).filter_by(id=emp.department_id).first()
    role = db.query(RoleORM).filter_by(id=emp.role_id).first()
    return employee_orm_to_pydantic(emp, dep, role)

@router.post("/employees", response_model=EmployeeOut, status_code=201, tags=["Employees"], summary="Create employee")
def create_new_employee(employee: EmployeeCreate, db: Session = Depends(get_db), request: Request = None):
    """
    Create a new employee record.

    Validates that department_id and role_id exist before creating the employee.
    Returns a user-friendly error message if they do not.
    Handles validation (400) and server errors (500) with clear client messages.
    """
    try:
        exists = db.query(EmployeeORM).filter_by(email=employee.email).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Validate Department
        dep = db.query(DepartmentORM).filter_by(id=employee.department_id).first()
        if not dep:
            raise HTTPException(status_code=400, detail=f"Department ID {employee.department_id} not found")

        # Validate Role
        role = db.query(RoleORM).filter_by(id=employee.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail=f"Role ID {employee.role_id} not found")

        if not employee.password or not isinstance(employee.password, str) or len(employee.password) < 1:
            raise HTTPException(status_code=400, detail="Password is required")

        # Defensive: Ensure all types match exactly for department_id/role_id
        dept_id = int(employee.department_id)
        role_id = int(employee.role_id)

        # Used explicit type conversion above to avoid type issues (e.g. with strings from JSON).
        hashed_pw = pwd_context.hash(employee.password)

        emp = EmployeeORM(
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            is_active=bool(employee.is_active),  # Defensive cast for booleans
            department_id=dept_id,
            role_id=role_id,
            hashed_password=hashed_pw,
            created_at=datetime.utcnow(),
        )
        db.add(emp)
        db.commit()
        db.refresh(emp)
        return employee_orm_to_pydantic(emp, dep, role)
    except HTTPException as e:
        # Client error, re-raise
        raise
    except ValidationError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Validation failed: {e.errors()}")
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Integrity error on employee creation: {str(e)}")
        raise HTTPException(status_code=400, detail="Database integrity error (possibly duplicate email or invalid related id).")
    except Exception as e:
        db.rollback()
        # Improved logging for debugging deeper type/mapping/column errors
        logger.error(f"Internal server error on /employees POST: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        # Send detailed message to help debug (strip in prod)
        detail_msg = f"Internal server error: {type(e).__name__}: {str(e)}"
        raise HTTPException(status_code=500, detail=detail_msg)

@router.put("/employees/{employee_id}", response_model=EmployeeOut, tags=["Employees"], summary="Update employee")
def update_employee_endpoint(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    """Update employee information."""
    emp = db.query(EmployeeORM).filter_by(id=employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    for field, value in employee.dict(exclude_unset=True).items():
        if field == "password":
            if value:
                setattr(emp, "hashed_password", pwd_context.hash(value))
        else:
            setattr(emp, field, value)
    db.commit()
    db.refresh(emp)
    dep = db.query(DepartmentORM).filter_by(id=emp.department_id).first()
    role = db.query(RoleORM).filter_by(id=emp.role_id).first()
    return employee_orm_to_pydantic(emp, dep, role)

@router.delete("/employees/{employee_id}", status_code=204, tags=["Employees"], summary="Delete employee")
def delete_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    """Delete an employee by ID."""
    emp = db.query(EmployeeORM).filter_by(id=employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return

# ---------------- Department Endpoints --------------------
@router.get("/departments", response_model=List[DepartmentOut], tags=["Departments"], summary="List all departments")
def list_departments(db: Session = Depends(get_db)):
    """List all departments."""
    return [department_orm_to_pydantic(dep) for dep in db.query(DepartmentORM).all()]

@router.post("/departments", response_model=DepartmentOut, status_code=201, tags=["Departments"], summary="Create a department")
def create_department(department: Department, db: Session = Depends(get_db)):
    """Create a new department."""
    if db.query(DepartmentORM).filter_by(id=department.id).first():
        raise HTTPException(status_code=400, detail="Department ID already exists")
    dep = DepartmentORM(id=department.id, name=department.name, description=department.description)
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return department_orm_to_pydantic(dep)

# ---------------- Role Endpoints --------------------
@router.get("/roles", response_model=List[RoleOut], tags=["Roles"], summary="List all roles")
def list_roles(db: Session = Depends(get_db)):
    """List all roles."""
    return [role_orm_to_pydantic(role) for role in db.query(RoleORM).all()]

@router.post("/roles", response_model=RoleOut, status_code=201, tags=["Roles"], summary="Create a role")
def create_role(role: Role, db: Session = Depends(get_db)):
    """Create a new role."""
    if db.query(RoleORM).filter_by(id=role.id).first():
        raise HTTPException(status_code=400, detail="Role ID already exists")
    roleobj = RoleORM(id=role.id, name=role.name, description=role.description)
    db.add(roleobj)
    db.commit()
    db.refresh(roleobj)
    return role_orm_to_pydantic(roleobj)
