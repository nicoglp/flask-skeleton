
from test import base
from app.base import schema as base_schema


class ParseFilterTestCase(base.BaseTestCase):

    def setUp(self):

       super(ParseFilterTestCase, self).setUp()
       self.schema = base_schema

    def test_parse_filter(self):

        filter = {
            "doctorId": "1235",
            "createAt": {"$gt": "12/12/12"},
            "$or":[
                {"state": "APPROVED"},
                {"state": {"$lt", "REJECTED"}}
            ]
        }
        filters = self.schema.parse_filter(filter)
        self.assertEqual(len(filters), 2)

        order = {
            "createAt": "desc",
            "userId": "asc"
        }
        orders = self.schema.parse_order(order)
        self.assertEqual(len(orders), 2)
