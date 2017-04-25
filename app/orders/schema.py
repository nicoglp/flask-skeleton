from marshmallow import fields, post_load

from app.base import schema
from app.phi.schema import PHISchema
from . import model


class OrderStateSchema(schema.BaseSchema):

    name = fields.String(required=True)
    description = fields.String(required=False)

    @post_load
    def make_object(self, data):
        return model.OrderState(**data)

order_state_schema = OrderStateSchema()


class StateMovementSchema(schema.BaseSchema):

    comments = fields.String(required=False)

    @post_load
    def make_object(self, data):
        return model.StateMovement(**data)

states_history_schema = StateMovementSchema()


class OrderSchema(PHISchema):
    """
    Generates fields based on the ``models.Order``
    which is a ``db.Model`` class from ``flask_sqlalchemy``.
    """

    deliveryId = fields.String(attribute="delivery_id",required=False, allow_none=True)
    actualStateId = fields.Integer(attribute="actual_state_id", required=False, allow_none=True)
    actualState = fields.Nested(OrderStateSchema, attribute="actual_state", required=False, allow_none=True)
    statesHistory = fields.Nested(StateMovementSchema, atribute='states_history', many=True, required=False, allow_none=True)


    @post_load
    def make_object(self, data):
        return model.Order(**data)

order_schema = OrderSchema()


