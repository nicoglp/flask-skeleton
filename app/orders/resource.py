import dao
import lib
import model
import schema
from app import api
from app.base import resource as base
from app.brac import require_auth
from app.phi import resource as phi


class OrderResource(phi.PHICollectionResource):
    def __init__(self, dao, schema, validators=None):
        base.CollectionResource.__init__(self, dao, schema, validators)

    @require_auth
    def post(self, **kwargs):
        """Create an order in ubiome an if it success creation, create an order in Ship Station"""
        # self._audit_before()

        order_response = phi.PHICollectionResource.post(self)
        order, errors = self.schema.loads(order_response.data)

        persistent_order = self.dao.retrieve(order.id)

        initial_state = model.ReadyToShipState()
        order.actual_state_id = initial_state.id
        order.actual_state = initial_state
        order.delivery_id = 'prueba'

        response = lib.create_ship_station_order(order)


        with self.dao.session_scope():
            order.change_state(response.json().get('orderStatus'))
            self.dao.update(order)

        print response.status_code

        return self._response(response.json(), 200)


api.add_resource(OrderResource,
                     '/shipOrder',
                     resource_class_args=(dao.order_dao, schema.order_schema),
                     endpoint='ShipOrderState::Search')


api.add_resource(phi.PHIEntityResource,
                 '/orders/<string:id>',
                 resource_class_args=(dao.order_dao, schema.order_schema),
                 endpoint='Order::Entity')


api.add_resource(phi.PHICollectionResource,
                 '/orders',
                 resource_class_args=(dao.order_dao, schema.order_schema),
                 endpoint='Order::Collection')

"""
api.add_resource(base.SearchResource,
                 '/search/kit-types',
                 resource_class_args=(dao.kit_type_dao, schema.kit_type_schema),
                 endpoint='KitType::Search')
"""