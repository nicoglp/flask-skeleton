import unittest
from app import service

class BaseTestCase(unittest.TestCase):
    """
    Base test case.
    Creates an Application Context for Flask interactions like access to `g` variable.
    """
    @classmethod
    def setUpClass(cls):
        # Client to test http resources/endpints
        cls.client = service.test_client()

    def setUp(self):
        self.app_context = service.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
