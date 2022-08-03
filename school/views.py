from django.http import request
from user.utils import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.response import Response

from user import permissions
from user.models import Person

from . import models, serializers
from django_filters.rest_framework import DjangoFilterBackend


class SchoolViewSets(viewsets.ModelViewSet):
    """
    get list of schools,retrive, create, fully-partially update and delete school
    authentication_classes = [jwt_authentication] ## Global set up in settings.base.py
    permission_classes = CRUD by role_id 1,2 & get by role_id 5,6
    """
    serializer_class = serializers.SchoolSerializer
    # filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filter_fields = ["is_active","school_code","school_name","email","contact_number"]
    search_fields = ["school_name", "is_active", "affiliation_no"]
    queryset = models.School.objects.all()
    permission_classes = [permissions.SchoolPermission]
    ordering_fields = ["school_name"]
    model = models.School
    lookup_field = "id"

    def get_serializer_class(self, *args, **kwargs):
        serializer = self.serializer_class
        if self.request.method in ["PUT", "PATCH"]:
            serializer = serializers.SchoolUpdateSerializer
        return serializer

    def get_queryset(self):
        queryset = self.queryset
        if self.request.auth in [3,4,5,6,7,8,9,10]:
            queryset = self.queryset.filter(school_code = self.request.user['school_code'])
        return queryset

    def create(self, request):
        ser = self.serializer_class(
            data=request.data, context={"authorized_by": request.user["id"]}
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(
            {"status": "success", "message": "school created", "data": ser.data},
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        ser = self.serializer_class(obj)
        response = {"status": "success", "message": "", "data": ser.data}
        return Response(response, status=status.HTTP_200_OK)

    def partial_update(self, request, id, *args, **kwargs):
        obj = get_object_or_404(self.model, id=id)
        ser = self.serializer_class(data=request.data, instance=obj, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        if ser.instance.is_active:
            Person.objects.filter(school_code=ser.instance.school_code).update(
                status="Approved"
            )
        response = {"status": "success", "message": "", "data": ser.data}
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, id, *args, **kwargs):
        obj = get_object_or_404(self.model, id=id)
        ser = self.serializer_class(data=request.data, instance=obj)
        ser.is_valid(raise_exception=True)
        ser.save()
        if ser.instance.is_active:
            Person.objects.filter(school_code=ser.instance.school_code).update(
                status="Approved"
            )
        response = {"status": "success", "message": "", "data": ser.data}
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        school = get_object_or_404(self.model, id=id)
        school.is_active = False
        Person.objects.filter(school_code=school.school_code).update(status="Discarded")
        school.save()
        return Response(
            {"status": "success", "id": id, "msg": "School deleted"},
            status=status.HTTP_200_OK,
        )
