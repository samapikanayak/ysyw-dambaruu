from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("standard", views.StandardViewSet, basename="standard")
router.register(
    "learning-outcome", views.LearningOutcomeViewSet, basename="learning-outcome"
)
router.register("subject", views.SubjectViewSet, basename="subject")
router.register("topic", views.TopicViewSet, basename="topic")
router.register("sub-topic", views.SubTopicViewSet, basename="sub-topic")
router.register("content",views.ContentViewSet,basename="content")
router.register("question",views.QuestionViewSet,basename="question")
urlpatterns = [
    path("", include(router.urls)),
]
