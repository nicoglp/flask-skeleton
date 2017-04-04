from app.brac import model
from test import base

class TestUserModelTestCase(base.BaseTestCase):

    def setUp(self):
        super(TestUserModelTestCase, self).setUp()

    def test_user_check_permission(self):

        user = model.BRACUser(ubiome_id='tv_id')
        self.assertFalse(user.has_persmision('User', 'C'))

        role_orders = model.Role(name="Medical")
        user.add_role(role_orders)
        self.assertFalse(user.has_persmision('User', 'C'))

        per1_user = model.Permission(resource='User', operations='CR')
        role_orders.add_permission(per1_user)
        self.assertTrue(user.has_persmision('User', 'C'))
        self.assertFalse(user.has_persmision('User', 'S'))

