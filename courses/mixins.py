from django.db.models import query
from user.utils import get_object_or_404
from rest_framework import status, viewsets,filters
from rest_framework.response import Response
from user import permissions
from user import models
from courses import models
from django.db import models,transaction
from rest_framework import serializers

class CourseMixin(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        context = {"created_by": request.user["id"]}
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.create_response["data"] = serializer.data
        return Response(self.create_response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        ser = self.serializer_class(obj)
        self.get_response["data"] = ser.data
        return Response(self.get_response, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=pk)
        ser = self.serializer_class(data=request.data, instance=obj, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        self.update_response["data"] = ser.data
        return Response(self.update_response, status=status.HTTP_200_OK)

    def update(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=pk)
        ser = self.serializer_class(data=request.data, instance=obj)
        ser.is_valid(raise_exception=True)
        ser.save()
        self.update_response["data"] = ser.data
        return Response(self.update_response, status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        self.delete_response["id"] = pk
        self.delete_response["data"] = None
        return Response(self.delete_response, status=status.HTTP_200_OK)



    
        