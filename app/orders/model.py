from marshmallow.fields import Integer
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import *

from app.base import model as base_model
from app.phi import model as phi_model
import datetime
import pytz

class OrderState(base_model.BaseDBModel):
    __tablename__ = 'order_states'
    # __abstract__ = True
    # __mapper_args__ = {
    #     'polymorphic_on': type,
    #     'polymorphic_identity': 'order_states'
    # }

    name = Column(String(128))
    description = Column(UnicodeText)
    type = Column(String(20))


class ReadyToShipState(OrderState):
    __mapper_args__ = {
        'polymorphic_identity': 'READY_TO_SHIP'
    }


class ShipOnCourseState(OrderState):
    __mapper_args__ = {
        'polymorphic_identity': 'ON_COURSE'
    }


class DeliveredState(OrderState):
    __mapper_args__ = {
        'polymorphic_identity': 'DELIVERED'
    }


class StateMovement(phi_model.PHIModel):
    __tablename__ = 'order_movements'

    def __init__(self, state):
        self.state = state

    comments = Column(String(256))
    state_id = Column('state_id', Integer, ForeignKey('order_states.id'))
    order_id = Column('order_id', String(32), ForeignKey('orders.id'))
    state = relationship(OrderState)
    order = relationship("Order")


class Order(phi_model.PHIModel):
    __tablename__ = 'orders'

    delivery_id = Column(String(256))
    actual_state_id = Column('actual_state_id', String(32), ForeignKey('order_states.id'))
    actual_state = relationship(OrderState)
    states_history = relationship("StateMovement", uselist=True)

    def change_state(self, state):
        state_movement = StateMovement(self.actual_state)
        state_movement.state = self.actual_state
        state_movement.order = self
        state_movement.modified_at = datetime.datetime.now(tz=pytz.utc)

        if not self.states_history:
            self.states_history = []

        self.states_history.append(state_movement)

        actual_state = OrderState()
        actual_state.name = state
        actual_state.description = state

        self.actual_state = actual_state
