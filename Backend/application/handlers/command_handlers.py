from uuid import UUID
from sqlalchemy.exc import IntegrityError, NoResultFound

from application.commands.create_cafe_command import CreateCafeCommand
from application.commands.update_cafe_command import UpdateCafeCommand
from application.commands.delete_cafe_command import DeleteCafeCommand

from application.commands.create_employee_command import CreateEmployeeCommand
from application.commands.update_employee_command import UpdateEmployeeCommand
from application.commands.delete_employee_command import DeleteEmployeeCommand

from application.interfaces.cafe_repository import ICafeRepository
from application.interfaces.employee_repository import IEmployeeRepository

from application.services.employee_id_generator import EmployeeIDGenerator

from domain.exceptions import DomainException

class CreateCafeCommandHandler:
    def __init__(self, cafe_repository: ICafeRepository):
        self.cafe_repository = cafe_repository

    def handle(self, command: CreateCafeCommand) -> UUID:
        cafe_data = command.model_dump(exclude_none = True)
        try:
            cafe_id = self.cafe_repository.add_cafe(cafe_data)
            return cafe_id
        except Exception as e:
            raise DomainException(f"Failed to create cafe: {str(e)}")
        
class UpdateCafeCommandHandler:
    def __init__(self, cafe_repository: ICafeRepository):
        self.cafe_repository = cafe_repository

    def handle(self, command: UpdateCafeCommand):
        update = command.model_dump(exclude_none=True, exclude={'id'})

        if not update:
            return
        
        try:
            self.cafe_repository.update_cafe(command.id, update)
        except NoResultFound:
            raise DomainException(f"Cafe with ID {command.id} not found.")
        except Exception as e:
            raise DomainException("Failed to updaate cafe")
        

class DeleteCafeCommandHandler:
    def __init__(self, cafe_repository: ICafeRepository):
        self.cafe_repository =  cafe_repository

    def handle(self, command: DeleteCafeCommand):
        try:
            self.cafe_repository.delete_cafe(command.id)
        except NoResultFound:
            raise DomainException(f"Cafe with ID {command.id} not found.")
        except Exception as e:
            raise DomainException("Failed to delete the cafe")
        

class CreateEmployeeCommandHandler:
    def __init__(self, employee_repository: IEmployeeRepository, cafe_repository: ICafeRepository, employee_id_generator: EmployeeIDGenerator):
        self.employee_repository = employee_repository
        self.cafe_repository = cafe_repository
        self.employee_id_generator = employee_id_generator

    def handle(self, command: CreateEmployeeCommand) -> str:
        if command.assigned_cafe_id:
            cafe = self.cafe_repository.get_cafe_by_id(command.assigned_cafe_id)
            if not cafe:
                raise DomainException(f"Assigned Cafe ID {command.assigned_cafe_id} does not exist")
        
        employee_id = self.employee_id_generator.generate_employee_id()
        employee_data = command.model_dump(exclude_none=True, exclude={'assigned_cafe_id'})

        try:
            self.employee_repository.add_employee(
                employee_id = employee_id,
                employee_data = employee_data,
                cafe_id = command.assigned_cafe_id
            )
            return employee_id
        except IntegrityError as e:
            raise DomainException(f"Failed to create employee due to integrity error {e}")
        except Exception as e:
            print("Error creating employee: {e}")
            raise DomainException("Failed to create employee due to server error")

class UpdateEmployeeCommandHandler:
        def __init__(self, employee_repository: IEmployeeRepository, cafe_repository: ICafeRepository):
            self.employee_repository = employee_repository
            self.cafe_repository = cafe_repository

        def handle(self, command: UpdateEmployeeCommand):
            if not self.employee_repository.get_employee_by_id(command.id):
                raise NoResultFound(f"Employee with ID {command.id} does not exist")
            
            if command.assigned_cafe_id:
                cafe = self.cafe_repository.get_cafe_by_id(command.assigned_cafe_id)
                if not cafe:
                    raise DomainException(f"Assigned Cafe ID {command.assigned_cafe_id} does not exist")
                
            employee_data = command.model_dump(exclude_none=True, exclude={'id', 'assigned_cafe_id'})

            try:
                self.employee_repository.update_employee(
                    employee_id = command.id,
                    employee_data = employee_data,
                    cafe_id = command.assigned_cafe_id
                )
            except IntegrityError as e: 
                raise DomainException("Failed to update employee due to data conflict (e.g., duplicate email/phone).")        
            except Exception as e:
                print(f"CRASH POINT: Unhandled error during repository call: {e}")
                raise DomainException("Failed to update the employee due to an unexpected internal error.")
            
class DeleteEmployeeCommandHandler:
    def __init__(self, employee_repository: IEmployeeRepository):
        self.employee_repository =  employee_repository

    def handle(self, command: DeleteEmployeeCommand):
        try:
            self.employee_repository.delete_employee(command.id)
        except NoResultFound:
            raise NoResultFound(f"Employee with ID {command.id} not found.")
        except Exception as e:
            print(f"Error deleting employee: {e}")
            raise DomainException("Failed to delete the employee.")