from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import *

from app.base import model as base_model
from app.phi import model as phi_model

class KitTypeTest(base_model.BaseDBModel):
    __tablename__ = 'kit_type_tests'

    test = Column(String(128))
    description = Column(UnicodeText)

class KitTypeOther(base_model.BaseDBModel):
    __tablename__ = 'kit_type_others'

    text = Column(String(128))
    description = Column(UnicodeText)

class KitType(base_model.BaseDBModel):
    __tablename__ = 'kit_types'

    name = Column(String(128))
    description = Column(UnicodeText)

    kit_type_test_id = Column('kit_type_test_id', String(32), ForeignKey('kit_type_tests.id'))
    kit_type_test = relationship(KitTypeTest)

    kit_type_other_id = Column('kit_type_other_id', String(32), ForeignKey('kit_type_others.id'))
    kit_type_other = relationship(KitTypeOther)


class Kit(phi_model.PHIModel):
    __tablename__ = 'kits'

    kit_type_id = Column('kit_type_id', String(32), ForeignKey('kit_types.id'))
    kit_type = relationship(KitType)

    barcode = Column('barcode', String(32))
    registered = Column('registered', DateTime)
    delivery_status = Column('delivery_status', String(32))


