import json

from test import brac
from app import service, api

from app.ping import resource
from app.ping import model


class TestChecker(model.HealthChecker):
    def __init__(self, active, mesg):
        self.active = active
        self.message = mesg

    def check(self):
        return [model.HealthResult(self.active, [self.message])]


api.add_resource(resource.PingResource,
                 '/ping',
                 endpoint='::Test Ping::',
                 resource_class_args=[model.CheckersWrapper([
                     TestChecker(True, 'True'),
                     TestChecker(False, 'False')
                 ])])


class TestPingResourceTestCase(brac.BRACTestCase):
    def test_ping(self):
        with brac.brac_scope():
            with service.test_client() as client:
                res = client.get(api.prefix + '/ping', content_type='application/json')

                self.assertEqual(res.status_code, 200)
                self.assertIsNotNone(json.loads(res.data))


class TestHealtchekTestCase(brac.BRACTestCase):
    def test_heartbeat(self):

            with service.test_client() as client:
                res = client.get('/heartbeat', content_type='application/json')

                self.assertEqual(res.status_code, 500)

