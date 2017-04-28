import datetime as dt
import requests
import model

def get_ship_station_url():
    return 'https://ssapi.shipstation.com/orders/createorder'


def get_headers():
    return {
            'Authorization': 'Basic YTcyNDE0YTZiOGUwNGRiYTg2NDI4YjQ1MjAzOGZkZmM6ZTUzMzFkZDhlZDRhNGZlNDk4YmIyMzIyMmIzNjQ1ZWE='}


def create_ship_station_order(order):
    now = dt.datetime.now()

    url = 'https://ssapi.shipstation.com/orders/createorder'
    order_request = {"orderNumber": "custom-id",
                       "orderDate": "2015-06-29T08:46:27.0000000",
                       "orderKey": order.id,
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
                               "lineItemKey": "vd08-MSLbtx",
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

    response = requests.post(url=url, headers=get_headers(), json=order_request)
    return response


# def get_state_from(ship_station_state):
#     return model.DeliveredState()


def get_state_from(ship_station_state):
    """case o if anidados que mapean los estados de shipStation a los de ubiome"""
    switcher = {
        "awaiting_payment": model.OnHoldState(),
        "awaiting_shipment": model.OnHoldState(),
        "shipped": model.DeliveredState(),
        "on_hold": model.ReadyToShipState(),
        "cancelled": model.CancelledState
    }
    return switcher.get(ship_station_state, None)

