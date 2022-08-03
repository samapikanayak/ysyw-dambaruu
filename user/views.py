from email.message import Message
from rest_framework import filters, generics, request,parsers
from rest_framework import serializers as rest_serializer
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models,serializers,authentications
from .utils import get_object_or_404, send_mail
from django.conf import settings
from django.contrib.auth.hashers import check_password,make_password
from . import models
import jwt
from datetime import datetime, timedelta
from .mixins import UserViewMixin
from .utils import send_sms


def date_calculation(dob):
    today = datetime.now()
    birth_date = datetime.strptime(dob,'%Y-%m-%d')
    print(f"{today=}")
    age = str((today - birth_date)/365)[:2] +" " + 'years'
    return age


class UserSignIn(generics.GenericAPIView):
    '''
    User signIn and get a token
    '''
    authentication_classes = [authentications.UserAuthentication,authentications.JWTAuthentication]
    def post(self,request):
        '''
        authentication_classes :- UserAuthentication :- request.user(token), request.auth(user detail)
        header = id:password(double base64 encoded).
        returns jwt token with user detail
        '''

        return Response({"status":"success","message":"login successful","token":request.user,"data":request.auth})
    def get(self,request):
        '''
        authentication_classes :- JWTAuthentication :- request.auth(user detail)
        header = token.
        returns :- user detail
        '''
        return Response({"status":"success","message":"login successful","data":request.auth})

    def put(self,request):
        return Response(request.user,status=request.auth)
      

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.LogInSerializer

    def get_authenticators(self):
        if self.request.method == "GET": self.authentication_classes.append(authentications.JWTAuthentication)
        elif self.request.method == "POST": self.authentication_classes.append(authentications.UserAuthentication)
        return super().get_authenticators()


class TestLogin(generics.GenericAPIView):
    serializer_class = serializers.TestLoginSerializer
    authentication_classes = []

    def post(self, request):
        if (
            person := models.Person.objects.filter(
                mobile_number=request.data["mobile_number"]
            )
        ).exists():
            token = person.first().token
            return Response({"status": "success", "token": token})
        else:
            return Response({"status": "login failed"})


class AdminViewSet(UserViewMixin):
    serializer_class = serializers.AdminSerializer
    model = models.Person
    lookup_field = "id"
    create_local = [5,6]
    user_role_id = [2,5,6]
    get_user = {
        1:[2,5,6],
        2:[5,6],
        5:[6],
    }


class TutorViewSet(UserViewMixin):
    serializer_class = serializers.TutorSerializer
    ordering_fields = ["created_at"]
    model = models.Person
    lookup_field = "id"
    create_local = [7]
    user_role_id = [3,7]
    get_user = {
        1:[3,7],
        2:[3,7],
        5:[7],
        6:[7],
    }


class StudentViewSet(UserViewMixin):
    serializer_class = serializers.StudentSerializer
    ordering_fields = ["created_at"]
    model = models.Person
    lookup_field = "id"
    create_local = [8]
    user_role_id = [4,8]
    get_user = {
        1:[4,8],
        2:[4,8],
        3:[4],
        5:[8],
        6:[8],
        7:[8],
        10:[8],
        9:[4,8],
    }


    
    def create(self, request):
        if mobile_number := request.data.get('mobile_number'):
            if not self.model.objects.filter(mobile_number=mobile_number).count() <= 4:
                raise rest_serializer.ValidationError({"mobile_number":["more than 4 Id can't be created with this number"]})
        if "role_id" in request.data:
            if dob:=request.data.get('date_of_birth'):
                context = {"age":date_calculation(dob),"date_of_birth":dob}
            if request.data["role_id"] == 8:
                return super().create(request) 
            elif request.data["role_id"] == 4:
                context = {"created_by": "","school_code":""}
            
                serialized_data = self.serializer_class(data=request.data, context=context)
                serialized_data.is_valid(raise_exception=True)
                serialized_data.save()
                student_serializer = serializers.StudentSerializer2(serialized_data.instance)
                return Response({"status": "success","message": "user created","data": student_serializer.data},status=status.HTTP_201_CREATED)
            
        else:
            raise rest_serializer.ValidationError({"role_id":["This field is required"]})
    

class ContentManagerViewSet(UserViewMixin):
    serializer_class = serializers.TutorSerializer
    ordering_fields = ["created_at"]
    model = models.Person
    lookup_field = "id"
    create_local = [10]
    user_role_id = [9,10]
    get_user = {
        1:[9,10],
        2:[9,10],
        5:[10],
        6:[10],
    }


class PersonPasswordSetAPIView(generics.GenericAPIView):
    serializer_class = serializers.PasswordSetSerializer
    authentication_classes = []
    permission_classes = []
    def post(self,request,id):
        serialzed_data = self.serializer_class(data=request.data)
        serialzed_data.is_valid(raise_exception=True)
        person = get_object_or_404(models.Person,"user",id=id)
        person.set_password(serialzed_data.data["password"])
        person.is_active = True
        person.status = "Approved"
        person.password_creation_token = ""
        person.save()
        return Response({"status":"success","message":"password set","data":None})


class ForgotPasswordEmail(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordSerializer
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        if person := models.Person.objects.filter(email=ser.data["email"]).first():
            time_delta = timedelta(days=0,hours=0,minutes=1,seconds=0)
            payload = {
                "id":ser.data['email'],
                "exp":datetime.utcnow()+ time_delta
            }
            #mail sent
            token = jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256').decode()
            person.reset_password_token = token
            link = settings.REACT_FRONTEND_PASSWORD_SET_URL + token
            person.save()
            # send_mail(body=link, to=person.email)

            return Response({"status":"success","message":f"a password reset mail has been sent to {ser.data['email']}","link":link,"data":None})
        return Response({"status":"failed","email":f"email does not exist","data":None})


class ForgotPasswordResetAPIView(generics.GenericAPIView):
    serializer_class = serializers.PasswordSetSerializer
    authentication_classes = []
    permission_classes = []
    def post(self,request,token):
        try:
            if person := models.Person.objects.filter(reset_password_token=token).first():
                payload = jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
                serialzed_data = self.serializer_class(data=request.data)
                serialzed_data.is_valid(raise_exception=True)
                person.set_password(serialzed_data.data["password"])
                person.reset_password_token = ""
                person.save()
                return Response({"status":"success","message":"password reset","data":None})
            return Response({"status":"failed","message":"link has been expired","data":None},status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"status":"failed","message":"link has been expired","data":None},status.HTTP_400_BAD_REQUEST)
        

class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    def post(self,request):
        ser = self.serializer_class(data=request.data)
        if not (person := models.Person.objects.filter(id=request.user["id"])).exists(): # only the logged in user can reset his password
            raise rest_serializer.ValidationError({"user":"user not found"})
        if not check_password(request.data["old_password"],person.first().password):
            raise rest_serializer.ValidationError({"password":"incorrect old password"})
        ser.is_valid(raise_exception=True)
        person = person.first()
        person.set_password(ser.data["password"])
        person.save()
        return Response({"status":"success","message":"password changed","data":None})


class GenerateOTP(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.VerifyOTPSerializer
    def post(self,request):
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        if mobile_number:=request.data['mobile_number']:
            if otp := models.OTP.objects.filter(mobile_number=mobile_number).first(): 
                otp.save()
            else:
                otp = models.OTP.objects.create(mobile_number=mobile_number)
            print(otp.otp)
            Message = f'Your OneTimePassword is {otp.otp}'
            PhoneNumber = "+91"+mobile_number
            # send_sms(to=PhoneNumber,body=Message)
            context = {
                "status":"success",
                "message":f"otp sent successfully to {otp.mobile_number}",
                "txn_id":otp.txn_id
            }
            return Response(context)


class ConfirmOTP(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.ConfirmOTPSerializer
    def post(self,request):
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        if ((otp := request.data.get('otp')) and (txn_id := request.data.get('txn_id'))):
            if otp == '5396':
            # if otp := models.OTP.objects.filter(txn_id=txn_id,otp=otp).first():
                if otp := models.OTP.objects.filter(txn_id=txn_id).first():
                    mobile_number = otp.mobile_number
                    if otp.is_verified:
                        if (person := models.Person.objects.filter(mobile_number=mobile_number)).exists():
                            '''roleId4(Global student) can login'''
                            person_data = serializers.StudentSerializer2(person,many=True).data
                            otp.delete()
                            return Response({"status":"success","message":f"otp verified","data":person_data})
                        else:
                            '''roleId4(Global student) can signup'''
                            return Response({"status":"success","message":f"otp verified.Please Signup","data":None})
        return Response({"status":"failed","message":f"invalid otp","data":None})


class GenerateTxnId(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.VerifyOTPSerializer
    def post(self,request):
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        if mobile_number:=request.data['mobile_number']:
            if otp := models.OTP.objects.filter(mobile_number=mobile_number).first(): 
                otp.save()
            else:
                otp = models.OTP.objects.create(mobile_number=mobile_number)
            print(otp.otp)
            context = {
                "status":"success",
                "message":f"succefully get txn_id",
                "txn_id":otp.txn_id
            }
            return Response(context)



class GetProfileFromTxn(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.RenderSerializer
    def post(self,request):
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        if txn_id := request.data.get('txn_id'):
            if otp := models.OTP.objects.filter(txn_id=txn_id).first():
                mobile_number = otp.mobile_number
                if (person := models.Person.objects.filter(mobile_number=mobile_number)).exists():
                    person_data = serializers.StudentSerializer2(person,many=True).data
                    return Response({"status":"success","message":f"otp verified","data":person_data})
                else:
                    return Response({"status":"success","message":f"otp verified.Please Signup","data":None})
        return Response({"status":"failed","message":f"invalid txn-id","data":None})
        
        
class profileAvatarViewset(viewsets.ModelViewSet):
    queryset = models.ProfileAvatar.objects.all()
    serializer_class = serializers.AvatarSeializar
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    authentication_classes = []
    permission_classes = []




            

            


