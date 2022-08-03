import re
from rest_framework.test import APITestCase
from django.urls import reverse
from .. models import Person, Role
from django.contrib.auth.hashers import make_password, check_password
import base64

class UserCreationTest(APITestCase):
    def setUp(self) -> None:
        self.role_1 = Role(role_id=1,role_name="Super Admin")
        self.role_2 = Role(role_id=2,role_name="Admin")
        self.role_3 = Role(role_id=3,role_name="Tutor")
        self.role_4 = Role(role_id=4,role_name="Student")
        self.role_5 = Role(role_id=5,role_name="Super Admin")
        self.role_6 = Role(role_id=6,role_name="Admin")
        self.role_7 = Role(role_id=7,role_name="Tutor")
        self.role_8 = Role(role_id=8,role_name="Student")
        self.role_9 = Role(role_id=9,role_name="Content Manager")
        self.role_10 = Role(role_id=10,role_name="Content Manager")

        self.role_1.save()
        self.role_2.save()
        self.role_3.save()
        self.role_4.save()
        self.role_5.save()
        self.role_6.save()
        self.role_7.save()
        self.role_8.save()
        self.role_9.save()
        self.role_10.save()

        

        self.admin = Person.objects.create(
            role_id=self.role_2,
            name="global",
            email="globaladmin12@gmail.com",
            mobile_number="78956",
            password=make_password("123456"),
            school_code="ysyw34",
            status="Approved"
        )
        return super().setUp()
        
class SignInTestCase(UserCreationTest):
    def test_signin_with_username_password(self):
        
        username = self.admin.email
        password = "123456"
        encoded_data = base64.b64encode(base64.b64encode(f"{username}:{password}".encode())).decode()
        header = {
            "HTTP_AUTHENTICATION":f"Authenticate {encoded_data}"
        }

        response = self.client.post(reverse("user-login"),**header)
        print(response.json())
        token = response.data["token"]
        assert 200 == response.status_code
        return token


    def test_get_user_detail(self):
        self.token = self.test_signin_with_username_password()
        header = {
            "HTTP_AUTHORIZATION":f"Bearer {self.token}"
        }
        response = self.client.get(reverse("user-login"),**header)
        assert 200 == response.status_code

 

        

    