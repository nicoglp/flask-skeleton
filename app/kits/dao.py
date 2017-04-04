from app import db
from app.base import dao as base
from app.phi import dao as phi
import model
import schema

class KitDAO(phi.PHIDAO):

    def __init__(self):
        phi.PHIDAO.__init__(self, model.Kit, schema.kit_schema)

    def find_by_user_id(self, user_id):
        return db.session.query(model.Kit).filter_by(user=user_id).all()

    def find_by_barcode(self, barcode):
        return db.session.query(model.Kit).filter_by(barcode=barcode).first()

kit_dao = KitDAO()


class KitTypeDAO(base.SQLAlchemyDAO):

    def __init__(self):
        base.SQLAlchemyDAO.__init__(self, model.KitType, schema.kit_type_schema)

kit_type_dao = KitTypeDAO()
