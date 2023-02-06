from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from db import db
from models import HiredEmployeeModel
from schemas import HiredEmployeeSchema, HiredEmployeeUpdateSchema

from azureblob import createClient, getContainerConnection, getlistBlobs, getDataframe

blp = Blueprint("HiredEmployees", "hiredemployees", description="Operations on HiredEmployees")


@blp.route("/hiredemployees/<int:hiredemployees_id>")
class HiredEmployee(MethodView):
    @jwt_required()
    @blp.response(200, HiredEmployeeSchema)
    def get(self, hiredemployee_id):
        hiredemployee = HiredEmployeeModel.query.get_or_404(hiredemployee_id)
        return hiredemployee

    @jwt_required()
    def delete(self, hiredemployee_id):
        hiredemployee = HiredEmployeeModel.query.get_or_404(hiredemployee_id)
        db.session.delete(hiredemployee)
        db.session.commit()
        return {"message": "Hired Employee deleted."}

    @jwt_required()
    @blp.arguments(HiredEmployeeUpdateSchema)
    @blp.response(200, HiredEmployeeSchema)
    def put(self, hiredemployee_data, hiredemployee_id):
        hiredemployee = HiredEmployeeModel.query.get(hiredemployee_id)

        if hiredemployee:
            hiredemployee.datetime = hiredemployee_data["datetime"]
            hiredemployee.name = hiredemployee_data["name"]
        else:
            hiredemployee = HiredEmployeeModel(id=hiredemployee_id, **hiredemployee_data)

        db.session.add(hiredemployee)
        db.session.commit()

        return hiredemployee


@blp.route("/hiredemployees")
class HiredEmployeeList(MethodView):
    #@jwt_required()
    @blp.response(200, HiredEmployeeSchema(many=True))
    def get(self):
        return HiredEmployeeModel.query.all()

    @jwt_required()
    @blp.arguments(HiredEmployeeSchema)
    @blp.response(201, HiredEmployeeSchema)
    def post(self, hiredemployee_data):
        hiredemployee = HiredEmployeeModel(**hiredemployee_data)

        try:
            db.session.add(hiredemployee)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the hiredemployee.")

        return 

@blp.route("/hiredemployees/ingest")
class HiredEmployeesIngest(MethodView):
    #@jwt_required()
    def get(self, containerName="hiredemployees"):
        try:
            client = createClient()
            containerConnection = getContainerConnection(client, containerName)
            listBlobs = getlistBlobs(containerConnection)
            df = getDataframe(listBlobs, containerName)
            df.rename(columns=dict(zip(df.columns, ["id","name", "datetime","department_id","job_id"]))).to_sql(name='hiredemployees', if_exists='append', chunksize=1000, con=db.engine, index=False)
            return {"message": "HiredEmployees csv Ingested"}, 201
        except IntegrityError as e:
            errorInfo = e.orig.args
            abort(
                400,
                message=f'Error code: {errorInfo[0]}'
            )