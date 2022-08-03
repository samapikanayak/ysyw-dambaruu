from string import digits
from wsgiref.validate import validator
from django.db import models
from django.forms import ImageField
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.conf import settings
import jwt, datetime
from django.contrib.auth.hashers import check_password, make_password
from django.core.validators import FileExtensionValidator
from uuid import uuid4


class CommonFields(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,unique=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.id)





class Role(models.Model):
    ROLE_CHOICES = [
        ("Super Admin", "SuperAdmin"),
        ("Admin", "Admin"),
        ("Tutor", "Tutor"),
        ("Student", "Student"),
        ("Super Admin", "SuperAdmin"),
        ("Admin", "Admin"),
        ("Tutor", "Tutor"),
        ("Student", "Student"),
        ("Content Manager", "Content Manager"),
        ("Content Manager", "Content Manager"),
    ]
    role_id = models.PositiveIntegerField(default=1, unique=True)
    role_name = models.CharField(
        max_length=40, choices=ROLE_CHOICES, default="Super Admin"
    )

    def __str__(self):
        return str(self.role_id)



class ProfileAvatar(models.Model):
    avatar = models.ImageField(upload_to = "image/avatar", validators=[FileExtensionValidator(allowed_extensions=['png','jpg'])])
    name = models.CharField(max_length=200, null=True)



class Person(CommonFields):
    student_approval_choice = [
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Discarded", "Discarded"),
    ]

    blood_group_choice = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    student_gender = [("Male", "Male"), ("Female", "Female"), ("Others", "Others")]

    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=12, null=True, blank=True)
    school_code = models.CharField(max_length=50, editable=False, blank=True)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    profile_picture = models.ForeignKey(ProfileAvatar,on_delete=models.PROTECT,null=True)
    mother_name = models.CharField(max_length=150, blank=True)
    father_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    age = models.CharField(max_length=12, blank=True, null=True)
    blood_group = models.CharField(max_length=4, choices=blood_group_choice, blank=True)
    gender = models.CharField(max_length=6, choices=student_gender, blank=True)
    student_id = models.CharField(max_length=150, editable=False, blank=True)
    standard = models.CharField(max_length=1000, blank=True, null=True)
    school_id = models.CharField(max_length=40, blank=True, null=True)
    mother_tongue = models.CharField(max_length=100, blank=True)
    language_comfortable_with = models.CharField(max_length=100, blank=True)
    learning_disability = models.CharField(max_length=100, blank=True)
    subjects_of_interest = models.CharField(max_length=100, blank=True)
    hobbies = models.CharField(max_length=100, blank=True)
    specific_health_issue_or_concern = models.CharField(max_length=100, blank=True)
    name_of_caregiver = models.CharField(max_length=100, blank=True)
    name_of_wellness_counseller = models.CharField(max_length=100, blank=True)
    location = models.TextField(blank=True, null=True)
    status = models.CharField(
        "Student Status",
        max_length=15,
        choices=student_approval_choice,
        default="Pending",
        blank=True,
    )
    school_name = models.CharField(max_length=60, blank=True, null=True)
    mail_sent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    login_otp = models.CharField(max_length=8, default="", blank=True, null=True)
    learning_domain = models.TextField(null=True, blank=True)
    password_creation_token = models.TextField(null=True,blank=True,unique=True)
    reset_password_token = models.TextField(null=True,blank=True)


    class Meta:
        db_table = "user"


    def save(self, *args, **kwargs):
        if self.role_id.role_id in [4, 8]:
            if not self.student_id:
                self.student_id = get_random_string(6)
                while Person.objects.filter(student_id=self.student_id).exists():
                    self.student_id = get_random_string(6)
                    '''
                    a token should be generated and sent in link during password creation and once password created it will be deleted
                    '''
        if not self.password_creation_token:
            self.password_creation_token = get_random_string(20)
            while Person.objects.filter(password_creation_token=self.password_creation_token).exists():
                self.password_creation_token = get_random_string(20)
        super(Person, self).save(*args, **kwargs)

    def set_password(self,password):
        self.password = make_password(password)

    def verify_password(self,password):
        if self.password:
            if check_password(password,self.password):
                return True
        return False

    @property
    def token(self):
        time_delta = datetime.timedelta(days=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_DAYS"],hours=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_HOURS"],minutes=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_MINUTES"],seconds=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_SECONDS"],)
        payload = {"id": str(self.id),"exp": datetime.datetime.utcnow() + time_delta,"role_id": self.role_id.role_id,"school_code": self.school_code}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256").decode()




   
class OTP(models.Model):
    otp_status_choices = [
        ('Intialize','Intialize'),
        ('Progress','Progress'),
        ('Complete','Complete'),
    ]


    mobile_number = models.CharField(max_length=10,null=True,blank=True)
    otp = models.CharField(max_length=10)
    time_stamp = models.DateTimeField()
    txn_id = models.UUIDField(editable=False,default=uuid4)
    otp_status = models.CharField(max_length=30,choices=otp_status_choices,default='Progress')

    def save(self,*args,**kwargs):
        self.otp = get_random_string(4,'0123456789')
        self.time_stamp = timezone.now() + datetime.timedelta(minutes=10)
        super(OTP,self).save(*args,**kwargs)

    @property
    def is_verified(self):
        exp_time = (self.time_stamp - timezone.now())
        if exp_time < datetime.timedelta(seconds=0):
            return False
        return True

        

