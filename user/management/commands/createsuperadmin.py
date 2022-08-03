import sys
from getpass import getpass

from django.core.management.base import BaseCommand

from user.models import Person, Role
from YourSkoolYourWay.utils import (check_password, email_validation,
                                      make_password, mobile_number_validation,
                                      password_validation, re)


def validate_password(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    mat = re.fullmatch(reg, password)
    if mat:
        return True
    return False


class Command(BaseCommand):
    help = "Create Super Admin"

    def handle(self, *args, **kwargs):
        try:
            role = Role.objects.get(role_id=1)
        except Role.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    "can not create super admin. First create super admin of role id 1 in Role table"
                )
            )
            sys.exit(0)
        name = input("Enter name: ")
        email = input("Enter email: ")
        while True:
            op, error = email_validation(email)
            if op:
                break
            self.stdout.write(self.style.ERROR(error))
            email = input("Enter email again: ")
        while True:
            self.stdout.write(
                self.style.WARNING(
                    "Password shoud contain at least 8 characters and maximum 20 charcater and should have minimum 1 special,uppercase,lowercase, digit character"
                )
            )
            password = getpass("Enter password: ")
            if validate_password(password):
                break

        cpassword = getpass("Confirm password: ")
        while password != cpassword:
            self.stdout.write(self.style.ERROR("password does not match"))
            cpassword = getpass("Confirm password: ")

        mobile_number = input("Enter mobile number: ")
        while True:
            op, error = mobile_number_validation(mobile_number)
            if op:
                break
            self.stdout.write(self.style.ERROR(error))
            mobile_number = input("Enter mobile number: ")
        school_code = input("Enter school code: ")
        while Person.objects.filter(school_code=school_code).exists():
            self.stdout.write(self.style.ERROR("school code exist"))
            school_code = input("Enter school code: ")
        Person(
            role_id=role,
            name=name,
            email=email,
            password=make_password(password),
            mobile_number=mobile_number,
            school_code=school_code,
            is_active=True,
            status="Approved",
        ).save()
        self.stdout.write(self.style.SUCCESS("super admin created successfully"))
