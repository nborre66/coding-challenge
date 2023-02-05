from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import JobModel
from schemas import JobSchema


blp = Blueprint("Jobs", "jobs", description="Operations on jobs")


@blp.route("/jobs/<int:job_id>")
class Job(MethodView):
    @jwt_required()
    @blp.response(200, JobSchema)
    def get(self, job_id):
        job = JobModel.query.get_or_404(job_id)
        return job
    
    @jwt_required()
    def delete(self, job_id):
        job = JobModel.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        return {"message": "Job deleted"}, 200


@blp.route("/jobs")
class JobList(MethodView):
    @jwt_required()
    @blp.response(200, JobSchema(many=True))
    def get(self):
        return JobModel.query.all()

    @jwt_required()
    @blp.arguments(JobSchema)
    @blp.response(201, JobSchema)
    def post(self, job_data):
        job = JobModel(**job_data)
        try:
            db.session.add(job)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A job with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the job.")

        return 