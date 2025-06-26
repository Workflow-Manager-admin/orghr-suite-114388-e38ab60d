from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
import os
from passlib.context import CryptContext

# SQLite DB file will reside in the root of the backend container
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "app_data.sqlite3")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- ORM MODELS ---

class DepartmentORM(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    employees = relationship("EmployeeORM", back_populates="department")

class RoleORM(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    employees = relationship("EmployeeORM", back_populates="role")

class EmployeeORM(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    hashed_password = Column(String, nullable=False)

    department = relationship("DepartmentORM", back_populates="employees")
    role = relationship("RoleORM", back_populates="employees")


def get_db():
    """Dependency to get a db session (close after request)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create tables and pre-seed roles, departments, and admin user if missing."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Predefined default data
    default_departments = [
        {"id": 1, "name": "HR", "description": "Human Resources"},
        {"id": 2, "name": "Engineering", "description": "Engineering Dept"}
    ]
    default_roles = [
        {"id": 1, "name": "Admin", "description": "Can manage system"},
        {"id": 2, "name": "Employee", "description": "Regular employee"}
    ]

    for dept in default_departments:
        obj = db.query(DepartmentORM).filter_by(id=dept["id"]).first()
        if not obj:
            db.add(DepartmentORM(**dept))

    for role in default_roles:
        obj = db.query(RoleORM).filter_by(id=role["id"]).first()
        if not obj:
            db.add(RoleORM(**role))

    db.commit()

    # Pre-seed default admin user
    admin_email = "admin@admin.com"
    admin_user = db.query(EmployeeORM).filter_by(email=admin_email).first()
    if not admin_user:
        hashed_pw = pwd_context.hash("admin")
        db.add(EmployeeORM(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            is_active=True,
            department_id=1,
            role_id=1,
            hashed_password=hashed_pw,
        ))
        db.commit()
    db.close()
