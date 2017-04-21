from marshmallow import fields, post_load

from app.base import schema
from app.phi.schema import PHISchema
from . import model


class OrderSchema(PHISchema):
    """
    Generates fields based on the ``models.Order``
    which is a ``db.Model`` class from ``flask_sqlalchemy``.
    """
    ownerId = fields.String(attribute="owner_id",required=True, allow_none=True)
    # orderId = fields.String(attribute="order_id",required=True, allow_none=True)
    actualState = fields.String(attribute="actual_state",required=True, allow_none=True)
    foreignOrderId = fields.String(attribute="foreign_order_id",required=False, allow_none=True)
    kits = fields.Raw()

    @post_load
    def make_object(self, data):
        return model.Order(**data)

order_schema = OrderSchema()