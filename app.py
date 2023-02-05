from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

import models

from db import db
from resources.job import blp as JobBlueprint
from resources.department import blp as DepartmentBlueprint
from resources.hiredemployees import blp as HiredEmployeeBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "91149598211353037690083917831700050517"
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(JobBlueprint)
    api.register_blueprint(DepartmentBlueprint)
    api.register_blueprint(HiredEmployeeBlueprint)

    return app