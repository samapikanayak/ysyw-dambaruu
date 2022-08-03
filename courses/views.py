from user.utils import get_object_or_404
from rest_framework import parsers,status
from rest_framework.response import Response
from user import permissions
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers
from .mixins import CourseMixin
from user.models import Person
from django.db.models import F
from user.authentications import IsAuthOrReadOnly
from school.models import School




class StandardViewSet(CourseMixin):
    filter_fields = ["standard_name"]
    authentication_classes = [IsAuthOrReadOnly]
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    # permission_classes = [permissions.AdminGlobalPermission]
    serializer_class = serializers.StandardSerializer
    model = models.Standard
    delete_response = {"status": "success", "message": "standard deleted"}
    update_response = {"status": "success", "message": "standard updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "standard created"}
    def get_queryset(self):
        queryset = models.Standard.objects.all()
        if self.request.auth in [4,8,9,10]:
            user = Person.objects.filter(id=self.request.user['id']).first()
            queryset = queryset.filter(standard_name__in=user.standard.split(','))
        elif self.request.auth in [5,6]:
            school = School.objects.filter(school_code=self.request.user['school_code']).first()
            queryset = queryset.filter(standard_name__in=school.classes.split(','))

        return queryset

class SubjectViewSet(CourseMixin):
    filter_fields = ["standard_id__standard_name","subject_name"]
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    permission_classes = []
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    model = models.Subject
    delete_response = {"status": "success", "message": "subject deleted"}
    update_response = {"status": "success", "message": "subject updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "subject created"}

class LearningOutcomeViewSet(CourseMixin):
    filter_fields = ["learning_outcome"]
    ordering = ["created_at"]
    queryset = models.LearningOutcome.objects.all()
    serializer_class = serializers.LearningOutcomeSerializer
    model = models.LearningOutcome
    delete_response = {"status": "success", "message": "learning outcome deleted"}
    update_response = {"status": "success", "message": "learning outcome updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "learning outcome created"}

class TopicViewSet(CourseMixin):
    queryset = models.Topic.objects.all()
    filter_fields = ["subject_id","topic_name", "topic_image"]
    serializer_class = serializers.TopicSerializer
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    permission_classes = []
    model = models.Topic
    delete_response = {"status": "success", "message": "topic deleted"}
    update_response = {"status": "success", "message": "topic updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "topic created"}

class SubTopicViewSet(CourseMixin):
    queryset = models.SubTopic.objects.all()
    filter_fields = ["topic_id","sub_topic_name"]
    serializer_class = serializers.SubTopicSerializer
    permission_classes = []
    model = models.SubTopic
    delete_response = {"status": "success", "message": "sub topic deleted"}
    update_response = {"status": "success", "message": "sub topic updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "sub topic created"}

class ContentViewSet(CourseMixin):
    queryset = models.Content.objects.all()
    filter_fields = ["standard_id","subject_id","topic_id","sub_topic_id","content_title","content_for","content_available_as"]
    serializer_class = serializers.ContentSerializer
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]

    permission_classes = []
    model = models.Content
    delete_response = {"status": "success", "message": "content deleted"}
    update_response = {"status": "success", "message": "content updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "content created"}
    def get_queryset(self):
        if self.request.auth in [4,8]:
            self.queryset = self.queryset.filter(content_for__in = ["Student", "All"])
        elif self.request.auth in [9,10]:
            self.queryset = self.queryset.filter(content_for__in = ["Teacher", "All"])
        return self.queryset


    def destroy(self,request,pk):
        try:
            content = models.Content.objects.get(id=pk)
            video_sequence = content.video_sequence
            contents = models.Content.objects.filter(sub_topic_id=content.sub_topic_id)
            contents = contents.filter(video_sequence__range=[video_sequence+1,contents.last().video_sequence+1])
            contents.update(video_sequence = F("video_sequence") - 1)
            content.delete()
            return Response({"status": "success", "message": "content deleted","response":pk, "data":None}, status=400)


        except models.Content.DoesNotExist:
            return Response({"status": "failed", "message": "content not found", "data":None}, status=400)

            

class QuestionViewSet(CourseMixin):
    queryset = models.ContentQuestion.objects.all()
    filter_fields = ["content_id"]
    model = models.ContentQuestion
    serializer_class = serializers.ContentQuestionSerializer
    delete_response = {"status": "success", "message": "content deleted"}
    update_response = {"status": "success", "message": "content updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "content created"}


  
