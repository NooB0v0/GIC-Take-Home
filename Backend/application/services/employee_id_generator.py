from typing import Optional, List
from sqlalchemy import Integer
from application.interfaces.employee_repository import IEmployeeRepository

class EmployeeIDGenerator:
    PREFIX = "UI"
    PADDING = 7

    def __init__(self, employee_repository: IEmployeeRepository):
        self.employee_repository = employee_repository

    def generate_employee_id(self) -> str:
        last_id = self.employee_repository.get_last_employee_id()

        next_id = last_id + 1
        id_num = str(next_id).zfill(self.PADDING)
        if (len(id_num)) > self.PADDING:
            raise OverflowError("Employee ID limit reached.")
    
        return f"{self.PREFIX}{id_num}"