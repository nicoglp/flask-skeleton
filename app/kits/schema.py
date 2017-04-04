from marshmallow import fields, post_load

from app.base import schema
from app.phi.schema import PHISchema
from . import model

class KitSchema(PHISchema):
    """
    Generates fields based on the ``models.Kit``
    which is a ``db.Model`` class from ``flask_sqlalchemy``.
    """
    kitTypeId = schema.UUID(attribute="kit_type_id", required=False, allow_none=True)

    barcode = fields.String(required=True, allow_none=True)
    registered = fields.Date()
    deliveryStatus = fields.String(attribute="delivery_status", required=True)

    @post_load
    def make_object(self, data):
        return model.Kit(**data)

kit_schema = KitSchema()


class KitTypeSchema(schema.BaseSchema):

    id = schema.UUID()

    # TODO Add a unique validation
    name = fields.String(required=True)

    description = fields.String()

    @post_load
    def make_object(self, data):
        return model.KitType(**data)

kit_type_schema = KitTypeSchema()