from django.db import models
from numpy import imag

from school.models import School

from user.models import CommonFields, Person

from moviepy.editor import VideoFileClip
import datetime

from django.core.validators import FileExtensionValidator

class Standard(CommonFields):
    standard_name = models.CharField(max_length=100, unique=True)
    price = models.FloatField(default=0)
    image = models.FileField(upload_to="image/courses_standard", null=True)

    class Meta:
        db_table = "standard"

    def __str__(self):
        return f"{self.standard_name}"


class LearningOutcome(CommonFields):
    learning_outcome = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = "learning_outcome"

    def __str__(self):
        return f"{self.learning_outcome}"


class Subject(CommonFields):
    standard_id = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE,
        related_name="standard_subjects",
        db_column="standard_id",
    )
    subject_name = models.CharField(max_length=50)
    subject_image = models.FileField(upload_to='image/course_subject',null=True,blank=True)

    class Meta:
        db_table = "subject"
      

    def __str__(self):
        return f"{self.subject_name} [ + {self.standard.standard_name} ]"


class Topic(CommonFields):
    subject_id = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="subject",
        db_column="subject_id",
    )
    topic_name = models.CharField(max_length=30, null= True)
    topic_image = models.ImageField(upload_to = "image/avatar", validators=[FileExtensionValidator(allowed_extensions=['png','jpg'])], null=True)

    class Meta:
        db_table = "topic"

    def __str__(self):
        return f"{self.topic_name} [  {self.subject.subject_name}] [ {self.subject.standard.standard_name}"


class SubTopic(CommonFields):
    topic_id = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="topic_subtopic",
        db_column="topic_id",
    )
    sub_topic_name = models.CharField(max_length=50)

    class Meta:
        db_table = "sub_topic"

    def __str__(self):
        return f"{self.sub_topic_name} {self.topic.topic_name} [ {self.topic.subject.subject_name}] [ {self.topic.subject.standard.standard_name}"


class Content(CommonFields):
    video_type = [("PDF", "PDF"), ("Video", "Video")]
    publishity = [("Publish", "Publish"), ("Unpublish", "Unpublish")]
    content_seen_to = [("Teacher", "Teacher"),("Student", "Student"),("All", "All")]
    video_paid_or_free = [("Free", "Free"), ("Paid", "Paid")]
    video_sequence = models.PositiveIntegerField(null=True,blank=True)
    standard_id = models.ForeignKey(Standard,on_delete=models.CASCADE,related_name="content_standard",db_column="standard_id",blank=True,null=True)
    subject_id = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="content_subject",db_column="subject_id",blank=True,null=True)
    topic_id = models.ForeignKey(Topic,on_delete=models.CASCADE,related_name="content_topic",db_column="topic_id",blank=True,null=True)
    sub_topic_id = models.ForeignKey(SubTopic,on_delete=models.CASCADE,related_name="content_sub_topic",db_column="sub_topic_id",blank=True,null=True)
    
    learning_outcome = models.CharField(max_length=30, null=True, blank=True)
    content_type = models.CharField(max_length=30, choices=video_type)
    content_title = models.CharField(max_length=90, null=True, blank=True)
    content_file = models.FileField(upload_to='video/course_content',null=True,blank=True)
    level = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=publishity)
    content_for = models.CharField(max_length=40,choices=content_seen_to,default="All",)
    content_available_as = models.CharField(max_length=10, choices=video_paid_or_free, default="Free")
    description = models.TextField(null=True, blank=True)
    thumbnail_image = models.FileField(upload_to='image/course_thumbnail',null=True,blank=True)
    video_duration = models.CharField(max_length=20,default='')
    video_paused_time = models.CharField(max_length=20,default='')

    def save(self, *args, **kwargs):
        if self.content_file.name.split('.')[-1].lower() in ["mp4","mkv","avi","wmv","mov"]:
            if not self.video_duration:
                self.video_duration = str(datetime.timedelta(seconds=VideoFileClip(self.content_file.file.temporary_file_path()).duration))
        super(Content,self).save(*args,**kwargs)



    def __str__(self):
        return f"{self.content_title}"

    class Meta:
        ordering = ["video_sequence"]
        db_table = "content"


class LearningOutcomeScore(CommonFields):
    learning_outcome = models.ForeignKey(
        LearningOutcome, on_delete=models.CASCADE, related_name="lc_score"
    )
    user = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="user_score"
    )
    score = models.FloatField()

    class Meta:
        db_table = "learning_outcome_score"


class ContentQuestion(CommonFields):
    content_id = models.ForeignKey(Content,on_delete=models.CASCADE,related_name="content_questions")
    question = models.TextField()
    answer = models.CharField(max_length=200)
    quiz_time_in_seconds = models.PositiveIntegerField()



    class Meta:
        db_table = "content_question"

class QuestionOption(CommonFields):
    question_id = models.ForeignKey(ContentQuestion,on_delete=models.CASCADE,related_name="options")
    text = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='image/options',null=True,blank=True)
        

