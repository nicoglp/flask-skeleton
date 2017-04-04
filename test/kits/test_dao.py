import datetime

from test.base import BaseTestCase
from test.brac import BRACTestCase, brac_scope

from app.kits import model
from app.kits import dao

class TestKitDAOTestCase(BRACTestCase):

    def setUp(self):
        super(TestKitDAOTestCase, self).setUp()
        self.dao = dao.kit_dao
        self.kit_dao = dao.kit_type_dao


    def test_create(self):
        with brac_scope({'Kit':'CRUD'}):

            kit_type = model.KitType(name = 'Test',
                                     description='Kit Type for Unit Tests',
                                     welcome_screen='<h1>Welcome</h1>',
                                     finish_screen='<h1>By</h1>')
            self.kit_dao.create(kit_type)

            kit = model.Kit(owner_id='0000',
                             registered=datetime.datetime.now(),
                             barcode='123456789',
                             kit_type = kit_type)

            kit_saved = self.dao.create(kit)
            self.assertIsNotNone(kit_saved.id)


            # Retrieve
            kit_retieved = self.dao.retrieve(kit_saved.id)
            self.assertIsNotNone(kit_retieved)
            self.assertEqual(kit_retieved, kit_saved)


            # Delete
            test_deleted = self.dao.delete(kit_retieved)
            self.assertIsNotNone(test_deleted)

            self.kit_dao.delete(kit_type)


class TestKitTypeDAO(BaseTestCase):

    def setUp(self):
        super(TestKitTypeDAO, self).setUp()
        self.dao = dao.kit_type_dao

    def test_create(self):

        kit_type = model.KitType(name = 'Test',
                                 description='Kit Type for Unit Tests',
                                 welcome_screen='<h1>Welcome</h1>',
                                 finish_screen='<h1>By</h1>')

        kit_saved = self.dao.create(kit_type)
        self.assertIsNotNone(kit_saved.id)


        # Retrieve
        kit_type_retieved = self.dao.retrieve(kit_saved.id)
        self.assertIsNotNone(kit_type_retieved)
        self.assertEqual(kit_type_retieved, kit_saved)


        # Delete
        test_deleted = self.dao.delete(kit_type_retieved)
        self.assertIsNotNone(test_deleted)