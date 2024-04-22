from django.db import models
from django.contrib.auth.models import User

from api_lessons.models import LessonCategory


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='profile_images', blank=True)
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.user.username


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(LessonCategory, on_delete=models.CASCADE)
    last_lesson_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} progress in {self.category.name}'


class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    periodic_lesson_reminders = models.BooleanField(default=True)
    friend_request_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f'Notification Settings for {self.user.username}'
