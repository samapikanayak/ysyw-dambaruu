from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("", views.SchoolViewSets, basename="school")


urlpatterns = [
    path("school/", include(router.urls)),
]
