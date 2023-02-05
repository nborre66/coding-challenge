from db import db


class DepartmentModel(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(80), unique=True, nullable=False)

    hiredemployees = db.relationship("HiredEmployeeModel", back_populates="department", lazy="dynamic")