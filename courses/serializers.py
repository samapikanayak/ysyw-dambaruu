from rest_framework import request, serializers

from user.models import Person

from . import models

from django.db.models import F

from django.db import transaction

from .utils import base64ToImage



class CommonSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(
        "get_created_by_name", read_only=True
    )

    def get_created_by_name(self, obj):
        if (person := Person.objects.filter(id=obj.created_by)).exists():
            return person.first().name
        return ""


class StandardSerializer(CommonSerializer):
    class Meta:
        model = models.Standard
        fields = ["id", "standard_name", "image","price","created_at", "created_by"]

    def validate(self, data):
        if "created_by" in self.context:
            data["created_by"] = self.context[
                "created_by"
            ]  # self.context["created_by"]returned from course.views.SchoolViewSets.create()
        return data


class LearningOutcomeSerializer(CommonSerializer):
    class Meta:
        model = models.LearningOutcome
        fields = ["id", "learning_outcome", "created_at", "created_by"]

    def validate(self, data):
        if "created_by" in self.context:
            data["created_by"] = self.context["created_by"]
        return data


class SubjectSerializer(CommonSerializer):
    standard_name = serializers.SerializerMethodField(
        "get_standard_name", read_only=True
    )

    class Meta:
        model = models.Subject
        fields = [
            "id",
            "standard_id",
            "subject_name",
            "subject_image",
            "created_at",
            "standard_name",
            "created_by",
        ]
        extra_kwargs = {"standard_id": {"write_only": True}}

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('standard_id', 'subject_name'),
                message="subject already exists"
            )
        ]

    def validate(self, data):
        if "created_by" in self.context:
            data["created_by"] = self.context["created_by"]
        return data


    def get_standard_name(self, obj):
        return obj.standard_id.standard_name


class TopicSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField("get_subject_name", read_only=True)

    class Meta:
        model = models.Topic
        fields = [
            "id",
            "subject_id",
            "topic_name",
            "topic_image",
            "subject_name",
            "created_by",
            "created_at",
        ]
        extra_kwargs = {"subject_id": {"write_only": True}}

    def validate(self, data):
        if "created_by" in self.context:
            data["created_by"] = self.context["created_by"]
        if models.Topic.objects.filter(
            subject_id=data.get("subject_id"), topic_name__iexact=data.get("topic_name")
        ).exists():
            raise serializers.ValidationError({"topic_name": "topic already exists"})
        return data

    def get_subject_name(selfself, obj):
        return obj.subject_id.subject_name


class SubTopicSerializer(CommonSerializer):
    topic_name = serializers.SerializerMethodField("get_topic_name", read_only=True)

    class Meta:
        model = models.SubTopic
        fields = [
            "id",
            "created_at",
            "topic_id",
            "sub_topic_name",
            "topic_name",
            "created_by",
        ]
        extra_kwargs = {"topic_id": {"write_only": True}}

    def validate(self, data):
        if "created_by" in self.context:
            data["created_by"] = self.context["created_by"]
        if models.SubTopic.objects.filter(
            sub_topic_name__iexact=data.get("sub_topic_name"),
            topic_id=data.get("topic_id"),
        ).exists():
            raise serializers.ValidationError({"sub_topic_name":"sub topic already exists"})
        return data

    def get_topic_name(self, obj):
        return obj.topic_id.topic_name


class Base64Field(serializers.CharField):
    class Meta:
        swagger_schema_fields = {
            "type": "string",
            'example':"imageBase64Encoded"
        }


       

class OptionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    image = Base64Field(required=False,write_only=True)
    image_url = serializers.SerializerMethodField('get_image_url',read_only=True)

    def get_image_url(self,obj):
        if obj.image != "":
            return obj.image.url
        return ""
    class Meta:
        model = models.QuestionOption
        fields = "__all__"
        extra_kwargs = {
            "question_id":{"read_only":True}
        }

class ContentQuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True,read_only=False)
    class Meta:
        model = models.ContentQuestion
        fields = ["content_id","id","question","answer",'quiz_time_in_seconds','options']
        

    def create(self,data):
        with transaction.atomic():
            options = None
            if "options" in data:
                options = data.pop('options')
            
            question = models.ContentQuestion.objects.create(**data)
            if options:
                for option in options:
                    if "id" in option:
                        option.pop("id")
                    if not any([option.get("text"),option.get('image')]):
                        raise serializers.ValidationError({"option":"Both option text and image should not be empty. Either one of hem"})
                        
                    if image := option.get("image"):
                        option['image'] = base64ToImage(image)
                    models.QuestionOption.objects.create(**option,question_id=question)
        return question

    def update(self,instance,data):
        with transaction.atomic():
            options = None
            if "options" in data:
                options = data.pop('options')
            instance.question = data.get("question",instance.question)
            instance.save()
            option_ids = instance.options.all().values("id")
            ids = [options_id['id'] for options_id in option_ids]
            if options:
                for option in options:
                    if (option_id := option.get('id',False)) not in ids:
                        raise serializers.ValidationError({"option_id":"option id not matched or not found"})                        
                    if image := option.get("image"):
                        if isinstance(image,str):...
                            # option = option.pop(option.get('image',instance.options.all()[0].image))
                        else:
                            option['image'] = base64ToImage(image)
                    # optionObj = Option.objects.get(id=o_id)
                    # optionObj.text = option.get('text',optionObj.text)
                    # optionObj.image = option.get('image',optionObj.image)
                    # optionObj.save()
                    models.QuestionOption.objects.filter(id=option_id).update(**option,question_id=instance)
        return instance





class ContentSerializer(serializers.ModelSerializer):
    content_questions = ContentQuestionSerializer(many=True,read_only=True)

    standard_name = serializers.SerializerMethodField(
        "get_standard_name", read_only=True
    )
    subject_name = serializers.SerializerMethodField(
        "get_subject_name", read_only=True
    )
    topic_name = serializers.SerializerMethodField(
        "get_topic_name", read_only=True
    )
    sub_topic_name = serializers.SerializerMethodField(
        "get_sub_topic_name", read_only=True
    )
    # content_questions = ContentQuestionSerializer(many=True, required=False)
    class Meta:
        model = models.Content
        fields = ['id',"content_title","content_file","video_duration","level","status","content_for","content_available_as","description","thumbnail_image","video_sequence","standard_id","standard_name","subject_id","subject_name","topic_id","topic_name","sub_topic_id","sub_topic_name","learning_outcome","content_type","content_questions"]
        
        extra_kwargs = {
            "video_sequence":{"required":False},
            "standard_id":{"write_only":True},
            "video_duration":{"read_only":True},
        }

    def create(self, validated_data):
        content_questions = {}
        if "content_questions" in validated_data:
            content_questions = validated_data.pop("content_questions")
        if 'video_sequence' in validated_data:
            validated_data.pop('video_sequence')
        video_sequence = models.Content.objects.all().count() + 1
        video_sequence = int(video_sequence)
        filter = {}
        if sub_topic_id := validated_data.get("sub_topic_id"):
            filter = {"sub_topic_id":sub_topic_id}
        if topic_id := validated_data.get("topic_id"):
            filter = {"topic_id":topic_id}
        if subject_id := validated_data.get("subject_id"):
            filter = {"subject_id":subject_id}
        if standard_id := validated_data.get("standard_id"):
            filter = {"standard_id":standard_id}

  
        video_sequence = models.Content.objects.filter(**filter).count()+1
        content = models.Content.objects.create(**validated_data,video_sequence=video_sequence)
        return content

    def update(self, instance, data):   
        content_question = {}
        if "content_questions" in data:
            content_question = data.pop("content_questions")
        if isinstance(data.get("content_file"),str):
            content_file = data.pop('content_file')
        if isinstance(data.get("thumbnail_image"),str):
            thumbnail_image = data.pop('thumbnail_image')
        instance.content_title = data.get('content_title',instance.content_title)
        instance.content_type = data.get('content_type',instance.content_type)
        instance.content_file = data.get('content_file',instance.content_file)
        instance.thumbnail_image = data.get('thumbnail_image',instance.thumbnail_image)
        instance.level = data.get('level',instance.level)
        instance.status = data.get('status',instance.status)
        instance.content_for = data.get('content_for',instance.content_for)
        instance.content_available_as = data.get('content_available_as',instance.content_available_as)
        instance.description = data.get('description',instance.description)
        instance.standard_id = data.get('standard_id',instance.standard_id)
        instance.subject_id = data.get('subject_id',instance.subject_id)
        instance.topic_id = data.get('topic_id',instance.topic_id)
        instance.sub_topic_id = data.get('sub_topic_id',instance.sub_topic_id)
        instance.learning_outcome = data.get('learning_outcome',instance.learning_outcome)
        
        if (video_sequence := data.get("video_sequence")):
            video_sequence = int(video_sequence)
            filter = {}
            if instance.sub_topic_id:
                filter = {"sub_topic_id":instance.sub_topic_id}
            if instance.topic_id:
                filter = {"topic_id":instance.topic_id}
            if instance.subject_id:
                filter = {"subject_id":instance.subject_id}
            if instance.standard_id:
                filter = {"standard_id":instance.standard_id}
            contents = models.Content.objects.filter(**filter)

            if video_sequence < instance.video_sequence:
                contents = contents.filter(video_sequence__range=[video_sequence,instance.video_sequence-1])
                contents.update(video_sequence = F("video_sequence") + 1)
            else:
                contents = contents.filter(video_sequence__range=[instance.video_sequence+1,video_sequence]) 
                contents.update(video_sequence = F("video_sequence") - 1)
        instance.save()
        return instance
        



    def get_standard_name(self, obj):
        if obj.standard_id:
            return obj.standard_id.standard_name
        return ""

    def get_subject_name(self, obj):
        if obj.subject_id:
            return obj.subject_id.subject_name
        return ""

    def get_topic_name(self, obj):
        if obj.topic_id:
            return obj.topic_id.topic_name
        return ""

    def get_sub_topic_name(self, obj):
        if obj.sub_topic_id:
            return obj.sub_topic_id.sub_topic_name
        return ""






























# class ContentSerializer(serializers.ModelSerializer):

#     standard_name = serializers.SerializerMethodField(
#         "get_standard_name", read_only=True
#     )
#     subject_name = serializers.SerializerMethodField(
#         "get_subject_name", read_only=True
#     )
#     topic_name = serializers.SerializerMethodField(
#         "get_topic_name", read_only=True
#     )
#     sub_topic_name = serializers.SerializerMethodField(
#         "get_sub_topic_name", read_only=True
#     )
#     # content_questions = ContentQuestionSerializer(many=True, required=False)
#     class Meta:
#         model = models.Content
#         fields = ['id',"content_title","content_file","level","status","content_for","content_available_as","description","thumbnail_image","video_sequence","standard_id","standard_name","subject_id","subject_name","topic_id","topic_name","sub_topic_id","sub_topic_name","learning_outcome","content_type"]
        
#         extra_kwargs = {
#             "video_sequence":{"required":False},
#             "standard_id":{"write_only":True},
#         }

#     def create(self, validated_data):
#         content_questions = {}
#         if "content_questions" in validated_data:
#             content_questions = validated_data.pop("content_questions")
#         if 'video_sequence' in validated_data:
#             validated_data.pop('video_sequence')
#         video_sequence = models.Content.objects.all().count() + 1
#         video_sequence = int(video_sequence)
#         filter = {}
#         if sub_topic_id := validated_data.get("sub_topic_id"):
#                 filter = {"sub_topic_id":sub_topic_id}
#         if topic_id := validated_data.get("topic_id"):
#                 filter = {"topic_id":topic_id}
#         if subject_id := validated_data.get("subject_id"):
#                 filter = {"subject_id":subject_id}
#         if standard_id := validated_data.get( "standard_id"):
#                 filter = {"standard_id":standard_id}

  
#         video_sequence = models.Content.objects.filter(**filter).count()+1
#         content = models.Content.objects.create(**validated_data,video_sequence=video_sequence)
#         if content_questions:
#             for question in content_questions:
#                 if "id" in question:
#                     question.pop("id")
#                 ContentQuestionSerializer(data=question).is_valid(raise_exception=True)
#                 question = models.ContentQuestion.objects.create(content_id=content, **question)
#         return content

#     def update(self, instance, data):   
#         content_question = {}
#         if "content_questions" in data:
#             content_question = data.pop("content_questions")
#         instance.content_title = data.get('content_title',instance.content_title)
#         instance.content_type = data.get('content_type',instance.content_type)
#         instance.content_file = data.get('content_file',instance.content_file)
#         instance.level = data.get('level',instance.level)
#         instance.status = data.get('status',instance.status)
#         instance.content_for = data.get('content_for',instance.content_for)
#         instance.content_available_as = data.get('content_available_as',instance.content_available_as)
#         instance.description = data.get('description',instance.description)
        
#         instance.standard_id = data.get('standard_id',instance.standard_id)
#         instance.subject_id = data.get('subject_id',instance.subject_id)
#         instance.topic_id = data.get('topic_id',instance.topic_id)
#         instance.sub_topic_id = data.get('sub_topic_id',instance.sub_topic_id)
#         instance.learning_outcome = data.get('learning_outcome',instance.learning_outcome)
        
#         if (video_sequence := data.get("video_sequence")):
#             video_sequence = int(video_sequence)
#             filter = {}
#             if instance.sub_topic_id:
#                 filter = {"sub_topic_id":instance.sub_topic_id}
#             if instance.topic_id:
#                 filter = {"topic_id":instance.topic_id}
#             if instance.subject_id:
#                 filter = {"subject_id":instance.subject_id}
#             if instance.standard_id:
#                 filter = {"standard_id":instance.standard_id}
#             contents = models.Content.objects.filter(**filter)

#             if video_sequence < instance.video_sequence:
#                 contents = contents.filter(video_sequence__range=[video_sequence,instance.video_sequence-1])
#                 contents.update(video_sequence = F("video_sequence") + 1)
#             else:
#                 contents = contents.filter(video_sequence__range=[instance.video_sequence+1,video_sequence]) 
#                 contents.update(video_sequence = F("video_sequence") - 1)
        
#         for questn in content_question:
#             if "id" in questn.keys():
#                 if question := models.ContentQuestion.objects.filter(id=questn['id']).first():
#                     ContentQuestionSerializer(data=questn).is_valid(raise_exception=True)
#                     question.answer = questn.get("answer",question.answer)
#                     question.question = questn.get("question",question.question)
#                     question.save()
#                 else:
#                     raise serializers.ValidationError({"id":"invalid content_id id"})
#             else:
#                 raise serializers.ValidationError({"id":"provide id"})
#         instance.save()
#         return instance



    # def content_delete(self):
    #     try:
    #         content = models.Content.objects.get(id=id)
    #         video_sequence = content.video_sequence
    #         contents = models.Content.objects.filter(sub_topic=content.sub_topic)
    #         contents = contents.filter(video_sequence__range=[video_sequence+1,contents.last().video_sequence+1])
    #         contents.update(video_sequence = F("video_sequence") - 1)
    #         content.delete()
    #         return {"status": "success", "msg": "content deleted", "response": id}, 200
    #     except models.Content.DoesNotExist:
    #         return {"status": "failed", "msg": "content doesnot exist"}, 400


#     def get_standard_name(self, obj):
#         if obj.standard_id:
#             return obj.standard_id.standard_name
#         return ""

#     def get_subject_name(self, obj):
#         if obj.subject_id:
#             return obj.subject_id.subject_name
#         return ""

#     def get_topic_name(self, obj):
#         if obj.topic_id:
#             return obj.topic_id.topic_name
#         return ""

#     def get_sub_topic_name(self, obj):
#         if obj.sub_topic_id:
#             return obj.sub_topic_id.sub_topic_name
#         return ""

