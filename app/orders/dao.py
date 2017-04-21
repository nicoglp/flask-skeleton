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
