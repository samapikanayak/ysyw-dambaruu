from django.contrib import admin

from .models import Standard, LearningOutcome, Subject, Topic, SubTopic, Content, LearningOutcomeScore, ContentQuestion, QuestionOption


@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'created_by', 'standard_name')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(LearningOutcome)
class LearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'created_by', 'learning_outcome')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'created_by',
        'standard_id',
        'subject_name',
        'subject_image',
    )
    list_filter = ('created_at', 'standard_id')
    date_hierarchy = 'created_at'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'created_by',
        'subject_id',
        'topic_name',
    )
    list_filter = ('created_at', 'subject_id')
    date_hierarchy = 'created_at'


@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'created_by',
        'topic_id',
        'sub_topic_name',
    )
    list_filter = ('created_at', 'topic_id')
    date_hierarchy = 'created_at'


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'created_by',
        'video_sequence',
        'standard_id',
        'subject_id',
        'topic_id',
        'sub_topic_id',
        'learning_outcome',
        'content_type',
        'content_title',
        'content_file',
        'level',
        'status',
        'content_for',
        'content_available_as',
        'description',
        'thumbnail_image',
    )
    list_filter = (
        'created_at',
        'standard_id',
        'subject_id',
        'topic_id',
        'sub_topic_id',
    )
    date_hierarchy = 'created_at'


@admin.register(LearningOutcomeScore)
class LearningOutcomeScoreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'created_by',
        'learning_outcome',
        'user',
        'score',
    )
    list_filter = ('created_at', 'learning_outcome', 'user')
    date_hierarchy = 'created_at'


@admin.register(ContentQuestion)
class ContentQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'created_by',
        'content_id',
        'question',
        'answer',
        'quiz_time_in_seconds',
    )
    list_filter = ('created_at', 'content_id')
    date_hierarchy = 'created_at'


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'created_by',
        'question_id',
        'text',
        'image',
    )
    list_filter = ('created_at', 'question_id')
    date_hierarchy = 'created_at'
