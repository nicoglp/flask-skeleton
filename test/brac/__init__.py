import flask
from contextlib import contextmanager

from test import base as test
from app import db
from app.user import model

class BRACTestCase(test.BaseTestCase):
    """
    Base test case for Base-Role Access Control
    Creates the 'brac' db schema for test user's permissions
    """
    @classmethod
    def setUpClass(cls):
        db.create_all()

    @classmethod
    def tearDownClass(self):
        db.drop_all()


@contextmanager
def brac_scope(perms={}):

    """Provide a User for a BRAC scope"""
    user = model.User(id='test')
    role_orders = model.Role(name="test")
    for entity, permissions in perms.iteritems():
        role_orders.add_permission(model.Permission(resource=entity, operations=permissions))
    user.add_role(role_orders)
    flask.g.user=user
    yield user
    flask.g.user=None