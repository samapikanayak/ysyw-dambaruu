import datetime
import re
from string import digits

from django.db import models
from django.utils.crypto import get_random_string

from user.models import CommonFields, Person


def generate_unique_school_code(school_name):
    tokens = school_name.split()
    string = ""
    for word in tokens:
        if word != "and":
            string += str(word[0])
    school_code = re.sub("[^A-Za-z0-9]+", "", string)
    return school_code


class School(CommonFields):
    school_name = models.CharField(max_length=50)
    school_head = models.CharField(max_length=50, default="")
    school_code = models.CharField(max_length=8)
    classes = models.CharField(max_length=30)
    address = models.TextField(blank=True)
    pin = models.CharField(max_length=6)
    city = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    affiliation_no = models.CharField(max_length=50, blank=True, null=True,unique=True)
    authorized_by = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "school"

    def __str__(self):
        return self.school_name

    def save(self, *args, **kwargs):
        if not self.school_code:
            self.school_code = generate_unique_school_code(self.school_name)
            while School.objects.filter(school_code=self.school_code).exists():
                self.school_code = (
                    generate_unique_school_code(self.school_name)
                    + get_random_string(2).upper()
                )
        super(School, self).save(*args, **kwargs)


class SuperAdminLocalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role_id__role_id=5)


class SuperAdminLocal(Person):
    objects = SuperAdminLocalManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Superadmin"


class AdminLocalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role_id__role_id=6)


class AdminLocal(Person):
    objects = AdminLocalManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Admin"


class TutorLocalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role_id__role_id=7)


class TutorLocal(Person):
    objects = TutorLocalManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Tutor"


class StudentLocalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role_id__role_id=8)


class StudentLocal(Person):
    objects = StudentLocalManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Student"
