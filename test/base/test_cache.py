import flask
from flask import Config
from mock import Mock, MagicMock

from app import service, cache
from app.brac import require_auth
from app.user import dao as user_dao, model
from test.brac import BRACTestCase, brac_scope


class TestRequiredAuthTestCase(BRACTestCase):

    def setUp(self):
        super(TestRequiredAuthTestCase, self).setUp()

    def test_cache(self):
            flask.g.user = None
            service.config['API_USER'] = 1
            flask.request = Mock(headers={})
            my_fn = Mock(name='my_fn')
            user_dao.user_dao = Mock()
            user_dao.user_dao.retrieve.return_value = model.User(id='test')
            wrapped = require_auth(my_fn)
            wrapped()
            self.assertEqual(flask.g.user.id, 'test')
            self.assertIsNotNone(cache.get("app.brac._get_cached_auth_user_memver"))