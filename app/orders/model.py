from marshmallow.fields import Integer
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import *

import lib
from app.base import model as base_model
from app.phi import model as phi_model


class OrderState(base_model.BaseDBModel):
    __tablename__ = 'order_states'

    name = Column(String(128))
    description = Column(UnicodeText)
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'order_states'
    }


class ReadyToShipState(OrderState):
    __mapper_args__ = {
        'polymorphic_identity': 'READY_TO_SHIP'
    }

    def __init__(self):
        self.id = 1


class ShipOnCourseState(OrderState):
    __mapper_args__ = {
        'polymorphic_identity': 'ON_COURSE'
    }

    def __init__(self):
        self.id = 2


class DeliveredState(OrderState):
    __mapper_args__ = {
        'polymorphic_identity': 'DELIVERED'
    }

    def __init__(self):
        self.id = 3


class StateMovement(phi_model.PHIModel):
    __tablename__ = 'order_movements'

    def __init__(self, state):
        self.state = state

    state_id = Column('state_id', Integer, ForeignKey('order_states.id'))
    order_id = Column('order_id', String(32), ForeignKey('orders.id'))
    state = relationship("OrderState", passive_updates=False)
    order = relationship("Order")


class Order(phi_model.PHIModel):
    __tablename__ = 'orders'

    delivery_id = Column(String(256))
    actual_state_id = Column('actual_state_id', String(32), ForeignKey('order_states.id'))
    actual_state = relationship(OrderState)
    states_history = relationship("StateMovement", uselist=True)

    def change_state(self, new_state):
        # state_movement = StateMovement(self.actual_state)
        # state_movement.order_id = self.id
        # state_movement.order = self
        # state_movement.modified_at = datetime.datetime.now(tz=pytz.utc)
        #
        # if not self.states_history:
        #     self.states_history = []
        #
        # self.states_history.append(state_movement)

        ubiome_state = lib.get_state_from(new_state)
        self.actual_state_id = ubiome_state.id

