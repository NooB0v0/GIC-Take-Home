from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

class IEmployeeRepository(ABC):
    @abstractmethod
    def get_all_employees(self, cafe_name: str) -> List[dict]:
        pass

    @abstractmethod
    def get_employee_by_id(self, employee_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def add_employee(self, employee_data: dict) -> dict:
        pass

    @abstractmethod
    def update_employee(self, employee_id: str, employee_data: dict) -> dict:
        pass

    @abstractmethod
    def delete_employee(self, employee_id: str) -> None:
        pass

    @abstractmethod
    def is_assigned_to_cafe(self, employee_id: str) -> bool:
        pass

    @abstractmethod
    def get_last_employee_id(self) -> Optional[int]:
        pass