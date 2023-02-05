from marshmallow import Schema, fields

class PlainHiredEmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    datetime = fields.DateTime(required=True)


class PlainJobSchema(Schema):
    id = fields.Int(dump_only=True)
    job = fields.Str()

class PlainDepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    department = fields.Str()

class HiredEmployeeSchema(PlainHiredEmployeeSchema):
    job_id = fields.Int(required=True, load_only=True)
    department_id = fields.Int(required=True, load_only=True)
    job = fields.Nested(PlainJobSchema(), dump_only=True)
    department = fields.Nested(PlainDepartmentSchema(), dump_only=True)


class HiredEmployeeUpdateSchema(Schema):
    name = fields.Str()
    datetime = fields.DateTime()


class JobSchema(PlainJobSchema):
    hiredEmployees = fields.List(fields.Nested(PlainHiredEmployeeSchema()), dump_only=True)

class DepartmentSchema(PlainDepartmentSchema):
    hiredEmployees = fields.List(fields.Nested(PlainHiredEmployeeSchema()), dump_only=True)

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str(load_only=True)