from flask_marshmallow import Schema
from marshmallow import fields


class HealthResultSchema(Schema):

    active = fields.Str()
    warnings = fields.List(fields.Str)

health_result = HealthResultSchema()