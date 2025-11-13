import os
from flask import Blueprint, request, jsonify
from injector import inject, Injector
from pydantic import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from application.mediator import Mediator
from application.commands.create_cafe_command import CreateCafeCommand
from application.commands.update_cafe_command import UpdateCafeCommand
from application.commands.delete_cafe_command import DeleteCafeCommand
from application.handlers.command_handlers import CreateCafeCommandHandler, UpdateCafeCommandHandler, DeleteCafeCommandHandler
from application.handlers.query_handlers import GetCafesQueryHandler
from application.queries.get_cafe_query import GetCafeQuery
from domain.exceptions import DomainException

cafe_blueprint = Blueprint('cafe', __name__)
UPLOAD_FOLDER = '/usr/src/app/public/logos'

class CafeController:
    @inject
    def __init__(self, mediator: Mediator, create_cafe_handler: CreateCafeCommandHandler, update_cafe_handler: UpdateCafeCommandHandler, delete_cafe_handler: DeleteCafeCommandHandler, get_cafes_handler: GetCafesQueryHandler):
        self.mediator = mediator
        self.create_cafe_handler = create_cafe_handler
        self.update_cafe_handler = update_cafe_handler
        self.delete_cafe_handler = delete_cafe_handler
        self.get_cafes_handler = get_cafes_handler

    def register_routes(self, app_injector: Injector):

        def get_controller():
            return app_injector.get(CafeController)
        
        @cafe_blueprint.route('/', methods=['POST'])
        def create_cafe():
            controller = get_controller()
            try:
                command_data = request.json
                command = CreateCafeCommand(**command_data)
                cafe_id = controller.create_cafe_handler.handle(command)
                return jsonify({"id": str(cafe_id), "message": "Cafe created successfully"}), 201
        
            except ValidationError as e:
                return jsonify({"error": e.errors()}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
        @cafe_blueprint.route('/<uuid:cafe_id>', methods=['PUT'])
        def update_cafe(cafe_id):
            controller = get_controller()
            try:
                command_data = request.json
                command = UpdateCafeCommand(id=cafe_id, **command_data)
                controller.update_cafe_handler.handle(command)
                return jsonify({"id": str(cafe_id), "message": "Cafe update successfully"}), 201
            
            except ValidationError as e:
                return jsonify({"error": e.errors()}), 400
            except NoResultFound:
                return jsonify({"error": f"Cafe with ID {cafe_id} not found."}), 404
            except Exception as e:
                if isinstance(e, DomainException):
                    return jsonify({"error": str(e)}), 400
                print(f"FATAL PYTHON ERROR during PUT: {e}") 
                return jsonify({"error": "Internal Server Error during update."}), 500
            
        @cafe_blueprint.route('/<uuid:cafe_id>', methods=['DELETE'])
        def delete_cafe(cafe_id):
            controller = get_controller()
            try:
                command = DeleteCafeCommand(id=cafe_id)
                controller.delete_cafe_handler.handle(command)
                return jsonify({"message": f"Cafe {cafe_id} deleted successfully"}), 204
            except Exception as e:
                return jsonify({"error": f"Failed to delete cafe: {str(e)}"}), 500
                
            
        @cafe_blueprint.route('/', methods=['GET'])
        def get_cafes():
            controller = get_controller()
            try:
                location = request.args.get('location')
                query = GetCafeQuery(location = location)
                cafe_list = controller.get_cafes_handler.handle(query)
                return jsonify(cafe_list), 200
            
            except Exception as e:
                return jsonify({'error': f"Failed to retrieve cafes: {str(e)}"}), 500
            

        @cafe_blueprint.route('/upload-logo/<string:cafe_id>', methods=['POST'])
        def upload_logo(cafe_id):
            if 'file' not in request.files:
                return jsonify({"error": "No file part in request"}), 400    
                   
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            
            if file:
                filename = secure_filename(file.filename)
                storage_folder = os.path.join(UPLOAD_FOLDER, cafe_id)
                os.makedirs(storage_folder, exist_ok=True)
                filepath = os.path.join(storage_folder, filename)
                file.save(filepath)
                new_filename = cafe_id + '/' + filename
                public_url = f'/logos/{new_filename}'
                
                return jsonify({"logoUrl": public_url}), 200

def init_app(app_injector: Injector):
    controller = app_injector.get(CafeController)
    controller.register_routes(app_injector)
    return cafe_blueprint