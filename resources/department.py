from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import DepartmentModel
from schemas import DepartmentSchema


blp = Blueprint("Departments", "depártments", description="Operations on departments")


@blp.route("/departments/<string:department_id>")
class Department(MethodView):
    @blp.response(200, DepartmentSchema)
    def get(self, department_id):
        department = DepartmentModel.query.get_or_404(department_id)
        return department

    def delete(self, department_id):
        department = DepartmentModel.query.get_or_404(department_id)
        db.session.delete(department)
        db.session.commit()
        return {"message": "Department deleted"}, 200


@blp.route("/departments")
class DepartmentList(MethodView):
    @blp.response(200, DepartmentSchema(many=True))
    def get(self):
        return DepartmentModel.query.all()

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