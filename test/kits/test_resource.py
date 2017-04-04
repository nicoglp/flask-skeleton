import json
from test import brac

from app import service, api



class TestKitResourceTestCase(brac.BRACTestCase):


    def test_kit_by_id(self):

        with brac.brac_scope({'Kit':'CRUD'}):
            with service.test_client() as client:

                res = client.get(api.prefix + '/kits',  content_type='application/json')
                self.assertEqual(res.status_code, 200)
                self.assertIsNotNone(json.loads(res.data))