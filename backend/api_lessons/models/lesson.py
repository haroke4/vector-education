from django.db import models
from api_users.models import UserModel


class LessonBatch(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.pk} Lesson Batch: {self.title}'


class Lesson(models.Model):
    lesson_batch = models.ForeignKey(LessonBatch, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    video_url = models.URLField()

    def __str__(self):
        return f'{self.pk} Lesson: {self.topic} '


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)

    def __str__(self):
        return f'{self.pk} Question'


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000, verbose_name='Ответ')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk} QuestionAnswer: {self.text}'


