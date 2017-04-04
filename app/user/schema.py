from app.base import schema as base_schema

from marshmallow import Schema, fields, post_load

from app.base import schema as base_schema

from . import model


class PermissionSchema(Schema):

    resource = fields.Str(attribute="resource")
    operations = fields.Str(attribute="operations")

    @post_load
    def make_object(self, data):
        return model.Permission(**data)


class RoleSchema(Schema):

    id= fields.Str()
    name = fields.Str(required=True, validate=base_schema.not_blank('name'))
    permissions = fields.Nested(PermissionSchema, many=True)

    @post_load
    def make_object(self, data):
        return model.Role(**data)


role_schema = RoleSchema()


class UserSchema(base_schema.BaseSchema):

    username = fields.Str(required=False, allow_none=True)  # Same as email
    status = fields.Str(required=False, allow_none=True)
    roles = fields.Nested(RoleSchema, many=True, exclude=('id', ))


    @post_load
    def make_object(self, data):
        return model.User(**data)

user_schema = UserSchema()
