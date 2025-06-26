from typing import Dict, List, Optional
from .models import Employee, Department, Role
from datetime import datetime

# Simple in-memory database. Swap with real DB/ORM as needed.
db_employees: Dict[int, Employee] = {}
db_departments: Dict[int, Department] = {
    1: Department(id=1, name="HR", description="Human Resources"),
    2: Department(id=2, name="Engineering", description="Engineering Dept"),
}
db_roles: Dict[int, Role] = {
    1: Role(id=1, name="Admin", description="Can manage system"),
    2: Role(id=2, name="Employee", description="Regular employee")
}
current_id = 1

def get_next_employee_id() -> int:
    global current_id
    current_id += 1
    return current_id

def create_employee(employee) -> Employee:
    eid = get_next_employee_id()
    emp = Employee(id=eid, created_at=datetime.now(), **employee.dict(exclude={'password'}))
    db_employees[eid] = emp
    return emp

def update_employee(employee_id, updates) -> Optional[Employee]:
    emp = db_employees.get(employee_id)
    if not emp:
        return None
    updated = emp.copy(update=updates.dict(exclude_unset=True))
    db_employees[employee_id] = updated
    return updated

def delete_employee(employee_id: int) -> bool:
    if employee_id in db_employees:
        del db_employees[employee_id]
        return True
    return False
