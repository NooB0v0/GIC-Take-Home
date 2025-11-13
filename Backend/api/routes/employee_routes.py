from flask import Blueprint, request, jsonify
from injector import inject, Injector
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound

from application.mediator import Mediator
from application.commands.create_employee_command import CreateEmployeeCommand
from application.commands.update_employee_command import UpdateEmployeeCommand
from application.commands.delete_employee_command import DeleteEmployeeCommand
from application.queries.get_employees_query import GetEmployeesQuery
from application.handlers.command_handlers import CreateEmployeeCommandHandler, UpdateEmployeeCommandHandler, DeleteEmployeeCommandHandler
from application.handlers.query_handlers import GetEmployeesQueryHandler

employee_blueprint = Blueprint('employee', __name__)

class EmployeeController:

    @inject
    def __init__(self, mediator: Mediator, create_employee_handler: CreateEmployeeCommandHandler, update_employee_handler: UpdateEmployeeCommandHandler, delete_employee_handler: DeleteEmployeeCommandHandler, get_employee_handler: GetEmployeesQueryHandler):
        self.mediator = mediator
        self.create_employee_handler = create_employee_handler
        self.update_employee_handler = update_employee_handler
        self.delete_employee_handler = delete_employee_handler
        self.get_employee_handler = get_employee_handler

    def register_routes(self, app_injector: Injector):
        def get_controller():
            return app_injector.get(EmployeeController)
        
        @employee_blueprint.route('/', methods=['POST'])
        def create_employee():
            controller = get_controller()
            try:
                command_data = request.json
                command = CreateEmployeeCommand(**command_data)
                employee_id = controller.create_employee_handler.handle(command)
                return jsonify({"id": employee_id, "message" : "Employee created and assigned successfully"}), 201
            
            except ValidationError as e:
                return jsonify({"error": e.errors()}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
        @employee_blueprint.route('/<string:employee_id>', methods=['PUT'])
        def update_employee(employee_id):
            controller = get_controller()
            try:
                command_data = request.json
                command = UpdateEmployeeCommand(id = employee_id, **command_data)
                controller.update_employee_handler.handle(command)
                return jsonify({"message": f"Employee {employee_id} updated successfully"}), 200
            
            except ValidationError as e:
                return jsonify({"error": e.errors()}), 400
            except Exception as e:
                return jsonify({"error": f"Failed to update employee: {str(e)}"}), 500
        
        @employee_blueprint.route('/<string:employee_id>', methods=['DELETE'])
        def delete_employee(employee_id):
            controller = get_controller()
            try:
                command = DeleteEmployeeCommand(id = employee_id)
                controller.delete_employee_handler.handle(command)
                return jsonify({"message": f"Employee {employee_id} deleted successfully"}), 204
            
            except Exception as e:
                return jsonify({"error": f"Failed to delete employee: {str(e)}"}), 500

        @employee_blueprint.route('/', methods=['GET'])
        def get_employee():
            controller = get_controller()
            try:
                cafe_name = request.args.get('cafe')
                query = GetEmployeesQuery(cafe_name=cafe_name)
                employee_list = controller.get_employee_handler.handle(query)
                return jsonify(employee_list), 200
            
            except ValidationError as e:
                return jsonify({'error': e.errors()}), 400
            except Exception as e:
                return jsonify({'error': f'Failed to retrieve employees: {str(e)}'}), 500
            
def init_app(app_injector: Injector):
    controller = app_injector.get(EmployeeController)
    controller.register_routes(app_injector)
    return employee_blueprint