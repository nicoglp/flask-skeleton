
from flask_sqlalchemy import Pagination
from marshmallow import ValidationError
from test import base
from app.base import schema


class PagintaionSchemaTestCase(base.BaseTestCase):


    def setUp(self):
       super(PagintaionSchemaTestCase, self).setUp()
       self.schema = schema.pagination_schema

    def test_dump(self):

        pagination = Pagination('', 5, 10, 48, [])
        try:
            pagination_dict, errors =  self.schema.dump(pagination)

            self.assertIsInstance(pagination_dict, dict)
            self.assertEqual(pagination.page, pagination_dict['pageNumber'])
            self.assertEqual(pagination.per_page, pagination_dict['pageSize'])
            self.assertEqual(pagination.total, pagination_dict['totalItems'])
            self.assertEqual(pagination.pages, pagination_dict['totalPages'])
            self.assertEqual(len(errors), 0)
        except ValidationError:
            self.fail()