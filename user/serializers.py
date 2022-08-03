from django.db.models import fields
from rest_framework import serializers

from courses.serializers import CommonSerializer
from school.models import School
import datetime
from .models import Person, Role, ProfileAvatar

from django.contrib.auth.hashers import check_password, make_password

from user import models

def date_calculation(dob):
    today = datetime.datetime.now()
    birth_date = datetime.datetime.strptime(dob,'%Y-%m-%d')
    print(f"{today=}")
    age = str((today - birth_date)/365)[:2] +" " + 'years'
    return age

class UserCommonSerailizer(CommonSerializer):
    mobile_number = serializers.RegexField(
        regex=r"^[6-9][0-9]",
        required=True,
        error_messages={"invalid": "invalid mobile number."},
    )

    #calls get_school_name method
    school_name = serializers.SerializerMethodField("get_school_name", read_only=True)


    def validate(self, data):
        '''
        validates user request data in body
        Parameters :-
            self - current object,
            data - dict, fields :- ["school_code","status","school_id","email","school_name","mother_name","father_name","language_comfortable_with","learning_disability","subjects_of_interest","blood_group","specific_health_issue_or_concern","hobbies","name_of_wellness_counseller","name_of_caregiver","location","learning_domain",]
        Returns :- validated data(dict)
        '''
        if "created_by" in self.context:
            data["created_by"] = self.context["created_by"]  # self.context["created_by"]returned from course.views.SchoolViewSets.create()
        if "role_id" in data:
            if data["role_id"].role_id in [5,6,7,8,10]:
                if "school_id" in data:
                    if (school := School.objects.filter(id=data["school_id"])).exists():
                        data["school_id"] = school.first().id
                        data["school_code"] = school.first().school_code
                    else:
                        raise serializers.ValidationError({"school_id":"school_id not found"})
            elif data['role_id'].role_id in [1,2,3,4,9]:
                if "school_id" in data:
                    data.pop("school_id")
                    if "school_code" in self.context:
                        data["school_code"] = self.context.get("school_code")
        if "date_of_birth" in self.context:
            data["age"] = self.context["age"]
        else:...
        return data

    def get_school_name(self, obj):
        '''
        retrive school_name of particular user from school_id
        Parameters:-
            self(current object),
            obj - person
        Returns :- 
            school_name{string}  
        '''
        if (school := School.objects.filter(id=obj.school_id)).exists():
            return school.first().school_name
        return ""


class TestLoginSerializer(serializers.Serializer):
    '''
    For developer's use during testing
    '''
    mobile_number = serializers.CharField(max_length=10)


class AdminSerializer(UserCommonSerailizer):
    '''
    serilization of Admin (role_id=1,2,5,6)data
    '''
    class Meta:
        model = Person
        fields = ["id","name","email","mobile_number","school_code","role_id","status","created_by","school_id","school_name",]

        extra_kwargs = {
            "school_code": {"read_only": True},
            "status": {"read_only": True},
            "school_id": {"required": False},
        }


class TutorSerializer(UserCommonSerailizer):
    '''
    serilization of Tutor(role_id= 3,7) data and ContentManager (role_id=9,10) data
    '''
    class Meta:
        model = Person
        fields = ["id","name","email","mobile_number","school_code","role_id","status","created_by","school_id","school_name","standard",]

        extra_kwargs = {
            "school_code": {"read_only": True},
            "status": {"read_only": True},
            "school_id": {"required": False},
        }


class StudentSerializer(UserCommonSerailizer):
    '''
    serilization of Student(role_id= 4,8) data 
    '''
    class Meta:
        model = Person
        fields = ["id","name","mobile_number","date_of_birth","age","school_code","role_id","status","school_id","standard", "profile_picture"]

        extra_kwargs = {
            "school_code": {"read_only": True},
            "id": {"read_only": True},
            "date_of_birth": {"required": False},
            "status": {"read_only": True},
            "school_id": {"required": False},
            # "email": {"required": False},
            "school_name": {"required": False},
            # "mother_name": {"required": False},
            # "father_name": {"required": False},
            # "language_comfortable_with": {"required": False},
            # "learning_disability": {"required": False},
            # "subjects_of_interest": {"required": False},
            # "blood_group": {"required": False},
            # "specific_health_issue_or_concern": {"required": False},
            # "hobbies": {"required": False},
            # "name_of_wellness_counseller": {"required": False},
            # "name_of_caregiver": {"required": False},
            # "location": {"required": False},
            # "learning_domain": {"required": False},
        }
    def validate(self,data):
        data["status"] = "Approved"
        return super().validate(data)
        

class PasswordSetSerializer(serializers.Serializer):

    password = serializers.CharField()
    confirm_password = serializers.CharField()
    def validate(self,data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password":"password and confirm password should match"})
        return data 


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate(self,data):
        if person:=Person.objects.filter(email=data["email"]).first():
            return data 
        raise serializers.ValidationError({"email":"email does not exist"})
        


class ChangePasswordSerializer(PasswordSetSerializer):
    old_password = serializers.CharField()
   

class VerifyOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10) 


class ConfirmOTPSerializer(serializers.Serializer):
    txn_id = serializers.CharField(max_length=1000) 
    otp = serializers.CharField(max_length=10)


class RenderSerializer(serializers.Serializer):
    txn_id = serializers.CharField(max_length=1000) 


class StudentSerializer2(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ['id','name','standard','token',"profile_picture"]


    def validate(self, data):
        return data

class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=200)

        

class AvatarSeializar(serializers.ModelSerializer):
    class Meta:
        model = ProfileAvatar
        fields = "__all__"

