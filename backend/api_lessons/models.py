from django.db import models
from api_users.models import UserModel


class Lesson(models.Model):
    CATEGORY_CHOICES = [
        ('Listening', 'Listening'),
        ('Reading', 'Reading'),
        ('Writing', 'Writing'),
        ('Speaking', 'Speaking'),
    ]

    topic = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video = models.URLField()
    lesson_number = models.PositiveIntegerField(blank=True, null=True)
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES
    )

    def save(self, *args, **kwargs):
        if (self.lesson_number is None) or (self.lesson_number - 1 > Lesson.objects.filter(category=self.category).count()):
            self.lesson_number = Lesson.objects.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic


class Progress(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    has_watched = models.BooleanField(default=False)


class AdditionalMaterial(models.Model):
    topic = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.topic
