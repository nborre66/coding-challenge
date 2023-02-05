from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import JobModel
from schemas import JobSchema


blp = Blueprint("Jobs", "jobs", description="Operations on jobs")


@blp.route("/jobs/<string:job_id>")
class Job(MethodView):
    @blp.response(200, JobSchema)
    def get(self, job_id):
        job = JobModel.query.get_or_404(job_id)
        return job

    def delete(self, job_id):
        job = JobModel.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        return {"message": "Job deleted"}, 200


@blp.route("/jobs")
class JobList(MethodView):
    @blp.response(200, JobSchema(many=True))
    def get(self):
        return JobModel.query.all()

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