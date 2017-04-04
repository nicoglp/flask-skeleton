import datetime
from marshmallow import ValidationError
from app.kits import schema
from app.kits import model
from test import base



class TestKitSchemaTestCase(base.BaseTestCase):


    def setUp(self):
        super(TestKitSchemaTestCase, self).setUp()
        self.schema = schema.kit_schema

    def test_dump(self):

        kit = model.Kit(owner_id='9999',
                         registered=datetime.datetime.now(),
                         barcode='123456789')
        try:
            kit_dict, errors =  self.schema.dump(kit)

            self.assertIsInstance(kit_dict, dict)
            self.assertEqual(len(errors), 0)
        except ValidationError:
            self.fail()


    def test_load(self):

        kit_dict = dict(
            user= '9999',
            registered='2016-01-22',
            barcode='123456789'
        )
        try:
            kit, errors =  self.schema.load(kit_dict)

            self.assertIsInstance(kit, model.Kit)
            self.assertEqual(len(errors), 0)
        except ValidationError:
            self.fail()