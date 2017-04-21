import flask
from app import api
from app.base import resource as base
from app.base import exception
from app.phi import resource as phi
import schema, dao
import requests



class OrderResource(base.EntityResource):

    def get(self, id, **kwargs):
        """ Search order state in shipStation"""
        self._audit_before()

        entity = self.dao.retrieve(id)
        if entity:
            headers = {'Authorization': 'Basic MWE2ZGJlZDdjZDA1NGM2NGEyNWVmNDlkMzcwM2FkNzE6NGJhOTliM2NhNWYzNDEyYTljOWM2YTExMzEzODMxNGE=' }
            https = "https://ssapi.shipstation.com/orders/{}".format(entity.foreign_order_id)
            response = requests.get(https, headers=headers)

            print response.json()
            return self._response(response.json(), 200)# esto debería mapearlo para obtener el estado
        else:
            raise exception.EntityNotFoundError(id)

    def post(self, id, **kwargs):
        """Create an order in Ship Station"""
        url = 'https://ssapi.shipstation.com/orders/createorder'
        ship_order = {"orderNumber": "custom-id",
                           "orderDate": "2017-04-16T08:46:27.0000000",
                           "orderKey": "custom-id",
                           "orderStatus": "awaiting_shipment",
                           "billTo": {
                               "name": "The President"
                           },
                           "shipTo": {
                               "name": "The President",
                               "company": "US Govt",
                               "street1": "1600 Pennsylvania Ave",
                               "street2": "Oval Office",
                               "city": "Washington",
                               "state": "DC",
                               "postalCode": "20500",
                               "country": "US",
                               "phone": "555-555-5555",
                               "residential": True
                           },
                           "items": [
                               {
                                   "lineItemKey": "test_item_key",
                                   "sku": "a-kit-barcode",
                                   "name": "Test item #2",
                                   "imageUrl": None,
                                   "weight": {
                                       "value": 24,
                                       "units": "ounces"
                                   },
                                   "quantity": 1,
                                   "unitPrice": 99.99,
                                   "taxAmount": 2.5,
                                   "shippingAmount": 5,
                                   "warehouseLocation": "Aisle 1, Bin 7",
                                   "options": [
                                       {
                                           "name": "Size",
                                           "value": "Large"
                                       }
                                   ],
                                   "productId": 123456,
                                   "fulfillmentSku": None,
                                   "adjustment": False,
                                   "upc": "32-65-98"
                               }]
                           }
        response = requests.post(url=url, headers=self._get_headers(), json=ship_order)
        foreign_order_id = response.json().get('orderId')
#       si retorna un 200 entonces debería buscar el Order local y actualizar el foreign_order_id


api.add_resource(OrderResource,
                 '/shipOrder/<string:id>',
                 resource_class_args=(dao.order_dao, schema.order_schema),
                 endpoint='ShipOrderState::Search')

api.add_resource(phi.PHIEntityResource,
                 '/orders/<string:id>',
                 resource_class_args=(dao.order_dao, schema.order_schema),
                 endpoint='Order::Entity')


api.add_resource(base.CollectionResource,
                 '/orders',
                 resource_class_args=(dao.order_dao, schema.order_schema),
                 endpoint='Order::Collection')

"""
api.add_resource(base.SearchResource,
                 '/search/kit-types',
                 resource_class_args=(dao.kit_type_dao, schema.kit_type_schema),
                 endpoint='KitType::Search')
"""