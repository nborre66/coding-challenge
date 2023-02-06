from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import DepartmentModel
from schemas import DepartmentSchema

from azureblob import createClient, getContainerConnection, getlistBlobs, getDataframe



blp = Blueprint("Departments", "departments", description="Operations on departments")


@blp.route("/departments/<int:department_id>")
class Department(MethodView):
    @jwt_required()
    @blp.response(200, DepartmentSchema)
    def get(self, department_id):
        department = DepartmentModel.query.get_or_404(department_id)
        return department
    
    @jwt_required()
    def delete(self, department_id):
        department = DepartmentModel.query.get_or_404(department_id)
        db.session.delete(department)
        db.session.commit()
        return {"message": "Department deleted"}, 200


@blp.route("/departments")
class DepartmentList(MethodView):
    @jwt_required()
    @blp.response(200, DepartmentSchema(many=True))
    def get(self):
        return DepartmentModel.query.all()

    @jwt_required()
    @blp.arguments(DepartmentSchema)
    @blp.response(201, DepartmentSchema)
    def post(self, department_data):
        department = DepartmentModel(**department_data)
        try:
            db.session.add(department)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A department with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the department.")

        return 

@blp.route("/departments/ingest")
class DepartmentIngest(MethodView):
    @jwt_required()
    def get(self, containerName="departments"):
        try:
            client = createClient()
            containerConnection = getContainerConnection(client, containerName)
            listBlobs = getlistBlobs(containerConnection)
            df = getDataframe(listBlobs, containerName)
            df.rename(columns=dict(zip(df.columns, ["id","department"]))).to_sql(name='departments', if_exists='append', chunksize=1000, con=db.engine, index=False)
            return {"message": "Department csv Ingested"}, 201
        except IntegrityError as e:
            errorInfo = e.orig.args
            abort(
                400,
                message=f'Error code: {errorInfo[0]}'
            )