from flask import Flask, jsonify, g, send_from_directory
from flask_cors import CORS
from injector import Injector

from api.routes import cafe_routes, employee_routes
from infrastructure.dependency.container import InfrastructureModule
from infrastructure.database.postgres import create_db_and_tables, wait_for_db

DB_INITIALIZED = False

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app)
    app_injector = Injector([InfrastructureModule()])

    wait_for_db()

    global DB_INITIALIZED
    if not DB_INITIALIZED:
        try:
            create_db_and_tables()
            DB_INITIALIZED = True
        except Exception as e:
            print(f"Error initializing database: {e}")

    def serve_uploaded_file(filename):
        return send_from_directory(
            directory = '/usr/src/app/public/logos',
            path = filename,
            mimetype = 'image/png' or 'image/jpeg'
        )

    app.register_blueprint(cafe_routes.init_app(app_injector), url_prefix='/cafes')
    app.register_blueprint(employee_routes.init_app(app_injector), url_prefix='/employees')
    
    app.add_url_rule(
        '/logos/<path:filename>',
        endpoint = 'uploaded_logos',
        view_func = serve_uploaded_file,
    )

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=5000)