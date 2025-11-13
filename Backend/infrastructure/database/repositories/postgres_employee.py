from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from sqlalchemy import func, select, delete, update, Date, Integer
from sqlalchemy.exc import NoResultFound, IntegrityError
from application.interfaces.employee_repository import IEmployeeRepository
from infrastructure.database.repositories.base_repository import BaseRepository
from infrastructure.database.sql_models import EmployeeModel, EmployeeCafeModel, CafeModel

class PostgresEmployeeRepository(BaseRepository, IEmployeeRepository):
    def get_all_employees(self, cafe_name: Optional[str] = None) -> List[dict]:
        days_worked = func.current_date() - func.cast(EmployeeCafeModel.start_date, Date)

        stmt = select(
            EmployeeModel.id,
            EmployeeModel.name,
            EmployeeModel.email_address,
            EmployeeModel.phone_number,
            EmployeeModel.gender,
            func.coalesce(days_worked, 0).label('days_worked'),
            EmployeeCafeModel.cafe_id,
            CafeModel.name.label('cafe_name'),
            ).outerjoin(
                EmployeeCafeModel, 
                EmployeeModel.id == EmployeeCafeModel.employee_id
                ).outerjoin(
                    CafeModel, 
                    EmployeeCafeModel.cafe_id == CafeModel.id
                    ).order_by(
                        func.coalesce(days_worked, 0).desc()
                        )
    
        if cafe_name:
            stmt = stmt.where(CafeModel.name == cafe_name)

        results = self.session.execute(stmt).mappings().all()
        return [dict(result) for result in results]

    def get_employee_by_id(self, employee_id: str) -> Optional[dict]:
        stmt = select(EmployeeModel).where(EmployeeModel.id == employee_id)
        try:
            result = self.session.scalar(stmt)
            if result:
                return result.__dict__
            else:
                return None
        except Exception:
            return None
        
    def add_employee(self, employee_id: str, employee_data: dict, cafe_id: UUID) -> dict:
        new_employee = EmployeeModel(id = employee_id, **employee_data)
        self.session.add(new_employee)
        if cafe_id:
            assignment = EmployeeCafeModel(
                employee_id = new_employee.id,
                cafe_id = cafe_id,
                start_date = date.today()
            )
            self.session.add(assignment)
        self.session.flush()
        return new_employee.id
    
    def update_employee(self, employee_id, employee_data, cafe_id: Optional[UUID]):
        stmt = update(EmployeeModel).where(EmployeeModel.id == employee_id).values(**employee_data)
        result = self.session.execute(stmt)

        if result.rowcount == 0:
            raise NoResultFound(f"Employee with ID {employee_id} not found")

        current_assignment_stmt = select(EmployeeCafeModel).where(EmployeeCafeModel.employee_id == employee_id)
        current_assignment = self.session.scalar(current_assignment_stmt)

        if cafe_id:
            if current_assignment:
                if current_assignment.cafe_id != cafe_id:
                    current_assignment.start_date = date.today()
                current_assignment.cafe_id = cafe_id
                self.session.flush()
            else:
                assignment = EmployeeCafeModel(
                    employee_id = employee_id,
                    cafe_id = cafe_id,
                    start_date = date.today()
                )
                self.session.add(assignment)
                self.session.flush()
        elif current_assignment:
            self.session.delete(current_assignment)
            self.session.flush()
    
    def delete_employee(self, employee_id: str):
        stmt = delete(EmployeeModel).where(EmployeeModel.id == employee_id)
        result = self.session.execute(stmt)
        if result.rowcount == 0:
            raise NoResultFound(f"Employee with id {employee_id} not found.")
        
    def is_assigned_to_cafe(self, employee_id: str) -> bool:
        stmt = select(EmployeeCafeModel).where(EmployeeCafeModel.employee_id == employee_id)
        result = self.session.scalar(stmt)
        if result:
            return True
        return False
    
    def get_last_employee_id(self) -> Optional[int]:
        employee_id_num = func.substring(EmployeeModel.id, 3).cast(Integer)
        stmt = select(func.max(employee_id_num))

        result = self.session.scalar(stmt)
        if result is not None:
            return result
        else:
            return 0