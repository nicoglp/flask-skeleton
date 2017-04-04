
from test import brac
from app import db
from app.base.dao import session_scope
from app.brac import model
from app.brac import dao

class TestUserDAOTestCase(brac.BRACTestCase):

    def setUp(self):
        super(TestUserDAOTestCase, self).setUp()
        self.user_dao = dao.user_dao
        self.role_dao = dao.role_dao

    def test_user_dao(self):

        with session_scope(rollback=True):
            user = model.BRACUser(ubiome_id = 'ABC')

            user_saved = self.user_dao.create(user)
            self.assertIsNotNone(user_saved.id)

            # Retrieve
            user_retrieved = self.user_dao.retrieve(user_saved.id)
            self.assertIsNotNone(user_retrieved)
            self.assertEqual(user_retrieved, user_saved)

            # Delete
            user_deleted = self.user_dao.delete(user_retrieved)
            self.assertIsNotNone(user_deleted)


class TestRoleDAOTestCase(brac.BRACTestCase):

    def setUp(self):
        super(TestRoleDAOTestCase, self).setUp()
        self.user_dao = dao.user_dao
        self.role_dao = dao.role_dao

    def test_role_dao(self):
        with session_scope(rollback=True):
            role = model.Role(name = 'ADMIN')
            role.add_permission(model.Permission(resource='users', operations='CR'))
            role_saved = self.role_dao.create(role)
            self.assertIsNotNone(role_saved.id)

            # Retrieve
            role_retieved = self.role_dao.retrieve(role_saved.id)
            self.assertIsNotNone(role_retieved)
            self.assertEqual(len(role_retieved.permissions),1)
            self.assertEqual(role_retieved, role_saved)

            # Delete
            role_deleted = self.role_dao.delete(role_retieved)
            self.assertIsNotNone(role_deleted)

            role_retieved_deleted = self.role_dao.retrieve(role_saved.id)
            self.assertIsNone(role_retieved_deleted)

    def test_roles_user_asignament(self):
        with session_scope(rollback=True):
            role = model.Role(name='ADMIN')
            saved_role = self.role_dao.create(role)

            user = model.BRACUser(ubiome_id = 'ABC')
            user.add_role(saved_role)
            user_saved = self.user_dao.create(user)

            # Retrieve
            user_retieved = self.user_dao.retrieve(user_saved.id)
            self.assertEqual(len(user_retieved.roles), 1)
            self.assertEqual(user_retieved, user_saved)

            # Delete
            user_deleted = self.user_dao.delete(user_retieved)
            role_deleted = self.role_dao.create(role)
            self.assertIsNotNone(user_deleted)
            self.assertIsNotNone(role_deleted)