import base64
import re
from datetime import datetime, timedelta

import jwt
from decouple import config
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Person
from user.serializers import AdminSerializer

from .permissions import course_permission_list, permissions_list



def get_username_password(encoded_data):
    try:
        original_data = base64.b64decode(base64.b64decode(encoded_data)).decode()
        if original_data:
            username, password = original_data.split(":")
            return username, password
        else:
            raise AuthenticationFailed("authentication failed")
    except base64.binascii.Error:
        raise AuthenticationFailed("authentication failed")
    except UnicodeDecodeError:
        raise AuthenticationFailed("authentication failed")
    except ValueError:
        raise AuthenticationFailed("authentication failed")


class AuthenticationFailed(Exception):
    def __init__(self, msg):
        self.msg = "authentication failed"


class AuthorizationFailed(Exception):
    def __init__(self, msg):
        self.msg = "authorization failed"
        super().__init__(self.msg)


class CrossAPIView(APIView):
    token = None
    id = None
    role_id = None
    school_code = None

    def check_permission(self, role_id, request):
        if role_id in permissions_list:
            self.permissions = permissions_list[role_id][request.method.lower()]
            return self.permissions
        if role_id in course_permission_list:
            course = ["standard", "subject", "topic", "subtopic", "content"]
            for i in course:
                self.course_permissions = course_permission_list[i][
                    request.method.lower()
                ]
                return self.permissions

        else:
            raise PermissionError("permission denied")

    def response(self, data, status):
        return Response(data, status=status)

    def get_token(self, person):
        if person.status == "Approved":
            if person.role_id.role_id in [1, 2, 5, 6]:
                serializer = AdminSerializer
            elif person.role_id.role_id in [3, 7]:
                serializer = AdminSerializer
            else:
                serializer = AdminSerializer
            td = timedelta(
                days=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_DAYS"],
                hours=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_HOURS"],
                minutes=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_MINUTES"],
                seconds=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_SECONDS"],
            )
            payload = {
                "id": person.id,
                "exp": datetime.utcnow() + td,
                "role_id": person.role_id.role_id,
                "school_code": person.school_code,
            }
            self.token = jwt.encode(payload, settings.SECRET_KEY, "HS256")
            self.person_serialized_data = serializer(person).data
            return self.token, self.person_serialized_data
        elif person.status == "Pending":
            raise AuthenticationFailed("kindly wait for approval")
        elif person.status == "Discarded":
            raise AuthenticationFailed(
                "your account has been discarded. kindly contact admin to activate your account"
            )

        else:
            raise AuthenticationFailed("kindly wait for approval")

    def authenticate(self, header_data=None, login_with_otp=False, person=None):
        try:
            if login_with_otp == False:
                prefix, encoded_data = header_data.split()
                if prefix == settings.JWT_AUTH["JWT_AUTHENTICATION_PREFIX"]:
                    username, password = get_username_password(encoded_data)
                if "@" in username:
                    person = Person.objects.filter(email=username)
                elif username.isdigit() and len(username) == 10:
                    person = Person.objects.filter(mobile_number=username)
                else:
                    if (
                        person := Person.objects.filter(
                            school_code=username, student_id=password
                        )
                    ).exists():
                        person = person.first()
                        self.get_token(person)
                        return self.token, self.person_serialized_data
                    else:
                        raise AuthenticationFailed("invalid school code or student id")

            if len(person) == 1:
                person = person.first()
                if login_with_otp:
                    person.login_otp = ""
                    person.save()
                    self.get_token(person)
                    return self.token, self.person_serialized_data
                else:
                    if check_password(password, person.password):
                        self.get_token(person)
                        return self.token, self.person_serialized_data
                    else:
                        raise AuthenticationFailed("wrong password")
            else:
                raise AuthenticationFailed("wrong email or mobile or school code")
        except ValueError:
            raise AuthenticationFailed("authentication failed")

    def authorize(self, header_data):
        try:
            prefix, token = header_data.split()
            if prefix == settings.JWT_AUTH["JWT_AUTHORIZATION_PREFIX"]:
                payload = jwt.decode(token, settings.SECRET_KEY, ["HS256"])
                self.id = payload["id"]
                self.role_id = payload["role_id"]
                self.school_code = payload["school_code"]
                return self.id, self.role_id, self.school_code
            else:
                raise AuthorizationFailed("authorization failed")
        except ValueError:
            raise AuthorizationFailed("authorization failed")
        except jwt.exceptions.DecodeError:
            raise AuthorizationFailed("authorization failed")
        except jwt.exceptions.InvalidSignatureError:
            raise AuthorizationFailed("authorization failed")
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthorizationFailed("token has been expired")
        except Person.DoesNotExist:
            raise AuthorizationFailed("authorization failed.no data found")
        except jwt.exceptions.InvalidTokenError:
            raise AuthorizationFailed("authorization failed")


def email_validation(email):
    regex = "[a-zA-Z]+.*@.+[.].+$"
    match = re.fullmatch(regex, email)
    if Person.objects.filter(email=email).exists():
        return False, "email already registerd"
    if not match:
        return False, "Invalid Email"
    return email, None


def password_validation(password):
    try:
        password = base64.b64decode(base64.b64decode(password)).decode()
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        mat = re.fullmatch(reg, password)
        if mat:
            return True, password
        return (
            False,
            "Password should have atleast 8 characters, one upper case, one lower case, one digit and one special character",
        )
    except base64.binascii.Error:
        return False, "Invalid Password format"
    except UnicodeDecodeError:
        return False, "Invalid Password format"


def mobile_number_validation(mobile):
    regex = "(0|91)?[6-9][0-9]{9}"
    match = re.fullmatch(regex, mobile)
    if match:
        if Person.objects.filter(mobile_number=mobile).exists():
            return False, "Mobile number already registered"
        return mobile, None
    return False, "Invalid Mobile Number"


def update_password_validation(old_password, new_password):
    try:
        old_password = base64.b64decode(base64.b64decode(old_password)).decode()
        new_password = base64.b64decode(base64.b64decode(new_password)).decode()
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        pat = re.compile(reg)
        mat = re.fullmatch(reg, new_password)
        if mat:
            return old_password, new_password
        return (
            False,
            "new password should have atleast 8 characters, one upper case, one lower case, one digit and one special character",
        )
    except base64.binascii.Error:
        return False, "Invalid Password format"
    except UnicodeDecodeError:
        return False, "Invalid Password format"


def paginate(request, queryset, Serializer):
    try:
        count = queryset.count()
        if len(queryset) == 0:
            return [], 0, "", ""
        if request.GET.get("size") == "all":
            serialized_data = Serializer(queryset, many=True).data
            next_page = ""
            previous_page = ""
        else:
            page_and_size = ["page", "size"]
            query_params = request.GET.dict().copy()
            for page_name in page_and_size:
                if page_name in query_params:
                    query_params.pop(page_name)
            other_query_params = ""
            for key, value in query_params.items():
                other_query_params += f"&{key}={value}"
            path = request.path
            host = request.get_host()
            http = "https://" if request.is_secure() else "http://"
            page = int(request.GET.get("page", settings.PAGINATION.get("page")))
            size = int(request.GET.get("size", settings.PAGINATION.get("page_size")))
            site = f"{http}{host}{path}"
            next_page = ""
            previous_page = ""
            if page == 1:
                if count > page * size:
                    next_page = (
                        site + f"?page={page + 1}&size={size}" + other_query_params
                    )
                else:
                    next_page = ""
            elif page * size > count:
                previous_page = ""
            elif page * size >= count:
                previous_page = (
                    site + f"?page={page - 1}&size={size}" + other_query_params
                )
            else:
                previous_page = (
                    site + f"?page={page - 1}&size={size}" + other_query_params
                )
                next_page = site + f"?page={page + 1}&size={size}" + other_query_params
            serialized_data = Serializer(
                queryset[page * size - size : page * size], many=True
            ).data
        return serialized_data, count, next_page, previous_page
    except ValueError:
        return None, None, "invalid page or size", "invalid page or size"
