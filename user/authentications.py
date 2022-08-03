from user.models import Person
import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from django.db.models import Q
from user import models, utils
import uuid

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request,get_login=None):
        try:
            if request.method == "POST" and "role_id" in request.data:
                if int(request.data["role_id"]) == 4:
                    return True,True
            prefix, token = request.META["HTTP_AUTHORIZATION"].split()
            if prefix == settings.JWT_AUTH["JWT_AUTHORIZATION_PREFIX"]:
                payload = jwt.decode(token, settings.SECRET_KEY, ["HS256"])
                if get_login:
                    if person := Person.objects.filter(id=payload['id']).first():
                        person_serialized_data = utils.get_token(person)
                        return True, person_serialized_data
                    raise exceptions.NotAuthenticated("authorization failed")
                return payload,payload["role_id"]  # payload=request.user and payload['role_id']=request.auth
            else:
                raise exceptions.NotAuthenticated("authorization failed")
        except (ValueError,KeyError,jwt.exceptions.DecodeError,jwt.exceptions.InvalidSignatureError,jwt.exceptions.ExpiredSignatureError,jwt.exceptions.InvalidTokenError):
            raise exceptions.NotAuthenticated("authorization failed")


class IsAuthOrReadOnly(JWTAuthentication):
    def authenticate(self, request):
        if request.method == "GET":
            return True ,True
        else:
            return super().authenticate(request)

class UserAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            if request.method == "GET":
                return super().authenticate(request,get_login=True)
            
            # header, encoded_data = request.META["HTTP_AUTHENTICATION"].split()
            # if header == settings.JWT_AUTH["JWT_AUTHENTICATION_PREFIX"]:
            username = request.data['username']
            password = request.data['password']
                # username, password = utils.get_username_password(encoded_data)
            if (person := models.Person.objects.filter(Q(mobile_number=username) | Q(email=username))).exists():
                person = person.first()
                '''
                LocalStudent(role_id=8) will login like GlobalStudent(roleId-4)
                '''
                if not person.verify_password(password):
                    raise exceptions.AuthenticationFailed("Password incorrect")
                serializer = utils.get_token(person)
                return person.token, serializer
            else:
                raise exceptions.AuthenticationFailed("Authetication failed1")
            # else:
            #     raise exceptions.AuthenticationFailed("Authetication failed2")
        except (KeyError,ValueError):
            raise exceptions.AuthenticationFailed("Autentication failed3")