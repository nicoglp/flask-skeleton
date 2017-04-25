import flask
from app import api
from app.base import resource as base
from app.base import exception
from app.phi import resource as phi
import schema, dao
import requests
import lib
import model
import json
from app.brac import require_auth

class OrderResource(phi.PHICollectionResource):
    def __init__(self, dao, schema, validators=None):
        base.CollectionResource.__init__(self, dao, schema, validators)

    @require_auth
    def post(self, **kwargs):
        """Create an order in ubiome an if it success creation, create an order in Ship Station"""
        self._audit_before()

        order_response = phi.PHICollectionResource.post(self)
        order, errors = self.schema.loads(order_response.data)

        response = lib.create_ship_station_order(order)

        with self.dao.session_scope():
            order.change_state(response.json().get('order_status'))
            self.dao.update(order)

        print response.status_code

        return self._response(response.json(), 200)

api.add_resource(OrderResource,
                     '/shipOrder',
                     resource_class_args=(dao.order_dao, schema.order_schema),
                     endpoint='ShipOrderState::Search')

# class OrderResource(base.CollectionResource):
#     def __init__(self, dao, schema, validators=None):
#         base.CollectionResource.__init__(self, dao, schema, validators)
#
#     def post(self, **kwargs):
#         """Create an order in ubiome an if it success creation, create an order in Ship Station"""
#         response = self.post(**kwargs) # quiero llamar al post de la super
#
#         si retorna que se cre la orden, la recupero y genero la orden para enviar a shipStation
#         order = self.dao.retrieve(id)
#
#         url = lib.get_ship_station_url()
#         ship_order = lib.get_ship_station_order(order)
#
#         response = requests.post(url=url, headers=self._get_headers(), json=ship_order)
#         delivery_id = response.json().get('orderId')
#         state = response.json().get('orderStatus')
#
#         state_movement = model.StateMovement()
#         # seteo todo lo de stateMovement
#
#         order.state_history.add(order.actual_state)
#
#         order.actual_state = state_movement
#
#         persisto la orden

        #       si retorna un 200 entonces debera buscar el Order local y actualizar el foreign_order_id



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