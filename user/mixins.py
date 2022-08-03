
from user import serializers
from rest_framework import serializers as rest_serializer
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models, permissions
from .utils import get_object_or_404
from django.conf import settings
from . import models
from django.conf import settings


class UserViewMixin(viewsets.ModelViewSet):
    '''
    list, create, retrive, partial-update, update, delete all users
    authentication_classes :- JWT authentication
    
    DjangoFilterBackend :- filters based on filter_fields in query_param
    SearchFilter :- searches based on search_field list in query_param
    OrderingFilter :- orders based on search_field list in query_param
    '''
    search_fields = ["email","mobile_number"]
    filter_fields = ["email","mobile_number","status","role_id","is_active","school_code","name"]
    permission_classes = [permissions.AdminGlobalPermission]

    ordering_fields = ["created_at"]
    ordering = ["created_at"]
    def create(self, request):
        '''
        override create method in order to set the created_by and school_code fields according to the loggedIn user
        Returns :-
             custom response (message,data,status)
        '''
        context = {"created_by": request.user["id"],"school_code":request.user["school_code"]}
        if mobile_number := request.data.get('mobile_number'):
            if not models.Person.objects.filter(mobile_number=mobile_number).count() <= 4:
                raise rest_serializer.ValidationError({"mobile_number":["Id can't be created with this number"]})
        if email := request.data.get("email"):
            if (person := models.Person.objects.filter(email=email)).exists():
                if person.first().name != request.data.get('name') and person.first().role_id.role_id == request.data.get(
                'role_id'):
                    raise rest_serializer.ValidationError({"email":["email already exists for this user"]})
        if role_id := int(request.data.get("role_id")):
            if role_id in self.user_role_id:
                if role_id in self.create_local:
                    if school_id := request.data.get("school_id"):
                        context["school_id"] = school_id
                    else:
                        raise rest_serializer.ValidationError(
                            {"school_id": ["This field is required"]}
                        )
            else:
                raise rest_serializer.ValidationError({"role_id":["invalid role_id for this user"]})
        else:
            raise rest_serializer.ValidationError({"role_id":["This field is required"]})
        serialized_data = self.serializer_class(data=request.data, context=context)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"status": "success", "message": "user created", "data": serialized_data.data,},status=status.HTTP_201_CREATED)

    def retrieve(self, request, id):
        obj = get_object_or_404(self.model , "user" ,id=id)
        serialized_data = self.serializer_class(obj)
        response = {"status": "success", "message": "", "data": serialized_data.data}
        return Response(response, status=status.HTTP_200_OK)

    def partial_update(self, request, id, *args, **kwargs):
        obj = get_object_or_404(self.model ,"user", id=id)
        serialized_data = self.serializer_class(
            data=request.data, instance=obj, partial=True
        )
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        response = {"status": "success","message": "user updated","data": serialized_data.data}
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, id, *args, **kwargs):
        obj = get_object_or_404(self.model ,"user", id=id)
        serialized_data = self.serializer_class(data=request.data, instance=obj)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        response = {"status": "success","message": "user updated","data": serialized_data.data}
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        user = get_object_or_404(self.model,"user", id=id,role_id__in=self.user_role_id)
        user.delete()
        return Response({"status": "success", "id": id, "msg": "user deleted", "data": None},status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.auth in self.__class__.get_user:
            queryset = models.Person.objects.filter(role_id__in = self.__class__.get_user[self.request.auth])
            if self.request.auth in [5,6,7,10]:
                queryset = queryset.filter(school_code=self.request.user["school_code"])
        else:
            queryset = models.Person.objects.none()
        return queryset

    


        
            