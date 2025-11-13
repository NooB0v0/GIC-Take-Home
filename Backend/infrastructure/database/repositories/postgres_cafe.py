from typing import List, Optional
from uuid import UUID
from sqlalchemy import func, select, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from application.interfaces.cafe_repository import ICafeRepository
from infrastructure.database.repositories.base_repository import BaseRepository
from infrastructure.database.sql_models import CafeModel, EmployeeCafeModel

class PostgresCafeRepository(BaseRepository, ICafeRepository):
    def get_all_cafes(self, location = None) -> List[dict]:
        employee_count = (
            select (
                EmployeeCafeModel.cafe_id, 
                func.count(EmployeeCafeModel.employee_id).label('employee_count')
            )
            .group_by(EmployeeCafeModel.cafe_id)
            .subquery()
        )
        stm = select(
            CafeModel.id,
            CafeModel.name,
            CafeModel.description,
            CafeModel.logo,
            CafeModel.location,
            func.coalesce(employee_count.c.employee_count, 0).label('employees')
        ).outerjoin(
            employee_count,
            CafeModel.id == employee_count.c.cafe_id
        ).order_by(
            func.coalesce(employee_count.c.employee_count, 0).desc()
        )

        if location:
            stm = stm.where(CafeModel.location == location)

        result = self.session.execute(stm).mappings().all()

        return [dict(row) for row in result]

    def get_cafe_by_id(self, cafe_id: UUID) -> dict:
        stmt = select(CafeModel).where(CafeModel.id == cafe_id)
        try:
            result = self.session.scalar(stmt)
            if result:
                return result.__dict__
            else:
                return None
        except Exception:
            return None

    def add_cafe(self, cafe_data: dict) -> UUID:
        new_cafe = CafeModel(**cafe_data)
        self.session.add(new_cafe)
        self.session.flush()
        return new_cafe.id
    
    def update_cafe(self, cafe_id: UUID, cafe_data: dict):
        try:
            stmt = update(CafeModel).where(CafeModel.id == cafe_id).values(**cafe_data)
            result = self.session.execute(stmt)
            if result.rowcount == 0:
                raise NoResultFound(f"Cafe with id {cafe_id} not found.")
        except IntegrityError as e:
            raise ValueError(f"Integrity error occurred: {str(e)}")
        except Exception as e:
            raise
    
    def delete_cafe(self, cafe_id: UUID) -> None:
        stmt = delete(CafeModel).where(CafeModel.id == cafe_id)
        result = self.session.execute(stmt)
        if result.rowcount == 0:
            raise NoResultFound(f"Cafe with id {cafe_id} not found.")
        
    