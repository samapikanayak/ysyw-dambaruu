from .. import models
from django.urls import reverse
from rest_framework.test import APITestCase

class SchoolAPITest(APITestCase):
    def test_school_creation(self):
        data = {
            "school_name"
        }
        response = self.client.post(reverse("school-list"))
        print(response)
        assert 200 == response.status_code