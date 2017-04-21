from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import *

from app.base import model as base_model
from app.phi import model as phi_model


class OrderState(base_model.BaseDBModel):
    __tablename__ = 'order_states'

    name = Column(String(128))
    description = Column(UnicodeText)


class Order(phi_model.PHIModel):
    __tablename__ = 'orders'

    owner_id = Column(String(36))
    actual_state = Column(String(50))
    foreign_order_id = Column(String(256))
   # actual_state = relationship(OrderState) this is useful if we model a hierarchy (State Pattern)
    kits = relationship("Kit", uselist=True)


# class PendingState(OrderState):
#     ""Its the Order initial state""
#
# class InCourseState(OrderState):
#
#
#
# class ShippedState(OrderState):
#
