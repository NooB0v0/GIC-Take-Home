from typing import List, Dict, Any

from application.queries.get_cafe_query import GetCafeQuery
from application.queries.get_employees_query import GetEmployeesQuery

from application.interfaces.cafe_repository import ICafeRepository
from application.interfaces.employee_repository import IEmployeeRepository

class GetCafesQueryHandler:
    def __init__(self, cafe_repository: ICafeRepository):
        self.cafe_repository = cafe_repository

    def handle(self, query: GetCafeQuery) -> List[Dict[str, Any]]:
        cafes_data = self.cafe_repository.get_all_cafes(location = query.location)
        return cafes_data
        

class GetEmployeesQueryHandler:
    def __init__(self, employee_repository: IEmployeeRepository):
        self.employee_repository = employee_repository

    def handle(self, query: GetEmployeesQuery) -> List[Dict[str, Any]]:
        employees_data = self.employee_repository.get_all_employees(cafe_name = query.cafe_name)
        return employees_data