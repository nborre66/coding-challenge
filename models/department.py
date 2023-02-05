from db import db


class DepartmentModel(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(80), unique=True, nullable=False)

    hired_employees = db.relationship("HiredEmployeeModel", back_populates="departments", lazy="dynamic")