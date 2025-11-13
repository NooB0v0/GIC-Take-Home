from injector import Module, provider, singleton, Injector
from sqlalchemy.orm import Session

from application.interfaces.employee_repository import IEmployeeRepository
from application.interfaces.cafe_repository import ICafeRepository
from application.services.employee_id_generator import EmployeeIDGenerator
from application.handlers.command_handlers import CreateCafeCommandHandler, UpdateCafeCommandHandler, DeleteCafeCommandHandler, CreateEmployeeCommandHandler, UpdateEmployeeCommandHandler, DeleteEmployeeCommandHandler
from application.handlers.query_handlers import GetCafesQueryHandler, GetEmployeesQueryHandler
from application.mediator import Mediator

from infrastructure.database.postgres import get_db
from infrastructure.database.repositories.postgres_employee import PostgresEmployeeRepository
from infrastructure.database.repositories.postgres_cafe import PostgresCafeRepository

class InfrastructureModule(Module):

    def configure(self, binder):
        binder.bind(Injector, to=Injector)

    @singleton
    @provider
    def provide_db_session(self) -> Session:
        for session in get_db():
            return session

    @singleton
    @provider
    def provide_employee_repository(self, db: Session) -> IEmployeeRepository:
        return PostgresEmployeeRepository(session=db)

    @singleton
    @provider
    def provide_cafe_repository(self, db: Session) -> ICafeRepository:
        return PostgresCafeRepository(session=db)
    
    @singleton
    @provider
    def provide_id_generator_service(self, employee_repository: IEmployeeRepository) -> EmployeeIDGenerator:
        return EmployeeIDGenerator(employee_repository=employee_repository)
    
    @singleton
    @provider
    def provide_create_cafe_command_handler(self, cafe_repository: ICafeRepository) -> CreateCafeCommandHandler:
        return CreateCafeCommandHandler(cafe_repository=cafe_repository)
    
    @singleton
    @provider
    def provide_update_cafe_command_handler(self, cafe_repository: ICafeRepository) -> UpdateCafeCommandHandler:
        return UpdateCafeCommandHandler(cafe_repository=cafe_repository)
    
    @singleton
    @provider
    def provide_delete_cafe_command_handler(self, cafe_repository: ICafeRepository) -> DeleteCafeCommandHandler:
        return DeleteCafeCommandHandler(cafe_repository=cafe_repository)

    @singleton
    @provider
    def provide_get_cafes_query_handler(self, cafe_repository: ICafeRepository) -> GetCafesQueryHandler:
        return GetCafesQueryHandler(cafe_repository=cafe_repository)
    
    @singleton
    @provider
    def provide_get_employees_query_handler(self, employee_repository: IEmployeeRepository) -> GetEmployeesQueryHandler:
        return GetEmployeesQueryHandler(employee_repository=employee_repository)
    
    @singleton
    @provider
    def provide_mediator(self, injector: Injector) -> Mediator:
        return Mediator(injector=injector)
    
    @singleton
    @provider
    def provide_create_employee_command_handler(self, employee_repository: IEmployeeRepository, cafe_repository: ICafeRepository, employee_id_generator: EmployeeIDGenerator) -> CreateEmployeeCommandHandler:
        return CreateEmployeeCommandHandler(employee_repository=employee_repository, cafe_repository=cafe_repository, employee_id_generator=employee_id_generator)
    
    @singleton
    @provider
    def provide_update_employee_command_handler(self, employee_repository: IEmployeeRepository, cafe_repository: ICafeRepository) -> UpdateEmployeeCommandHandler:
        return UpdateEmployeeCommandHandler(employee_repository=employee_repository, cafe_repository=cafe_repository)
    
    @singleton
    @provider
    def provide_delete_employee_command_handler(self, employee_repository: IEmployeeRepository) -> DeleteEmployeeCommandHandler:
        return DeleteEmployeeCommandHandler(employee_repository=employee_repository)