from db import db


class HiredEmployeeModel(db.Model):
    __tablename__ = "hiredemployees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    datetime = db.Column(db.DateTime, unique=False, nullable=False)

    department_id = db.Column(
        db.Integer, db.ForeignKey("departments.id"), unique=False, nullable=False
    )
    department = db.relationship("DepartmentModel", back_populates="hiredemployees")
    
    job_id = db.Column(
        db.Integer, db.ForeignKey("jobs.id"), unique=False, nullable=False
    )
    job = db.relationship("JobModel", back_populates="hiredemployees")