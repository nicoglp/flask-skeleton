from app import db
from app.base import dao as base
from app.phi import dao as phi
import model
import schema


class OrderDAO(phi.PHIDAO):

    def __init__(self):
        phi.PHIDAO.__init__(self, model.Order, schema.order_schema)

    def find_by_owner(self, owner_id):
        return db.session.query(model.Order).filter_by(user=owner_id).all()

order_dao = OrderDAO()


class OrderStateDAO(base.SQLAlchemyDAO):

    def __init__(self):
        base.SQLAlchemyDAO.__init__(self, model.OrderState, schema.order_state_schema)

order_state_dao = OrderStateDAO()


class StateHistoryDAO(base.SQLAlchemyDAO):

    def __init__(self):
        base.SQLAlchemyDAO.__init__(self, model.StateMovement, schema.states_history_schema)

states_history_dao = StateHistoryDAO()
