from uuid import uuid4
from sqlalchemy import Column, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

class EmployeeModel(Base):
    __tablename__ = 'employee'

    id = Column(String(9), primary_key=True)
    name = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=False)
    phone_number = Column(String(8), nullable=False)
    gender = Column(String(8), nullable=False)

    assignments = relationship("EmployeeCafeModel", back_populates='employee', cascade="all, delete-orphan")

class CafeModel(Base):
    __tablename__ = 'cafe'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    logo = Column(String, nullable=True)
    location = Column(String(255), nullable=False)

    assignments = relationship("EmployeeCafeModel", back_populates='cafe', cascade="all, delete-orphan")

class EmployeeCafeModel(Base):
    __tablename__ = 'employee_cafe'
    __table_args__ = (UniqueConstraint('employee_id', 'cafe_id', name='uix_employee_cafe'),)

    employee_id = Column(String(9), ForeignKey('employee.id', ondelete='CASCADE'), primary_key=True)
    cafe_id = Column(UUID(as_uuid=True), ForeignKey('cafe.id', ondelete='CASCADE'), primary_key=True)
    start_date = Column(Date, nullable=False)

    employee = relationship("EmployeeModel", back_populates='assignments')
    cafe = relationship("CafeModel", back_populates='assignments')