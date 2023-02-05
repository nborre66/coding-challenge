from db import db


class JobModel(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(80), unique=True, nullable=False)

    hired_employees = db.relationship("HiredEmployeeModel", back_populates="jobs", lazy="dynamic")