from django.test import TestCase

from .models import Registration


class EmployeeTest(TestCase):
    def setUp(self):
        person = Registration.objects.create(
            username="8976", otp="1234", is_verified=False
        )
        print("Number of Person")

    def test_person_count(self):
        ss = Registration.objects.all()
        self.assertEquals(ss.count(), 1)
