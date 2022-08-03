import sys

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError, OperationalError

from user.models import Role


class Command(BaseCommand):
    help = "Create Roles of different user"

    def handle(self, *args, **kwargs):
        try:
            if not Role.objects.filter(role_id=1).exists():
                Role(role_id=1, role_name="Super Admin").save()
            if not Role.objects.filter(role_id=2).exists():
                Role(role_id=2, role_name="Admin").save()
            if not Role.objects.filter(role_id=3).exists():
                Role(role_id=3, role_name="Tutor").save()
            if not Role.objects.filter(role_id=4).exists():
                Role(role_id=4, role_name="Student").save()
            if not Role.objects.filter(role_id=5).exists():
                Role(role_id=5, role_name="Super Admin").save()
            if not Role.objects.filter(role_id=6).exists():
                Role(role_id=6, role_name="Admin").save()
            if not Role.objects.filter(role_id=7).exists():
                Role(role_id=7, role_name="Tutor").save()
            if not Role.objects.filter(role_id=8).exists():
                Role(role_id=8, role_name="Student").save()
            if not Role.objects.filter(role_id=9).exists():
                Role(role_id=9, role_name="Content Manager").save()
            if not Role.objects.filter(role_id=10).exists():
                Role(role_id=10, role_name="Content Manager").save()
            self.stdout.write(
                self.style.SUCCESS("All user role created successfully..")
            )
        except OperationalError:
            self.stdout.write(
                self.style.ERROR(
                    'No Role table found. First create the table by "python manage.py migrate command"'
                )
            )
            sys.exit(0)
        except IntegrityError:
            self.stdout.write(self.style.ERROR("Role has been already created."))
