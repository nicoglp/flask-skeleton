from marshmallow import fields

from app.base import schema
from app.user.dao import user_dao

class PHISchema(schema.BaseSchema):
    
    def __init__(self, **kwargs):
        super(PHISchema, self).__init__(**kwargs)

    userId = schema.UUID(attribute='owner_id', validate=schema.entity_exist('userId', user_dao), required=False, allow_none=True)
    createdAt = fields.DateTime(format='iso8601', attribute='created_at', dump_only=True)
    modifiedAt = fields.DateTime(format='iso8601', attribute='modified_at', dump_only=True)
    modifiedBy = fields.Str(attribute='modified_by', dump_only=True)
