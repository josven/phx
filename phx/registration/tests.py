from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse_lazy


class TestRegistrationViews(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_startpage(self):
        response = self.client.get(reverse_lazy('start'))
        self.assertEqual(response.status_code, 200)
