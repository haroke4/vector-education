from django.db import models
from api_users.models import CustomUser
from api_lessons.models import LessonCategory


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='profile_images', blank=True)
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.user.username


class NotificationSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    periodic_lesson_reminders = models.BooleanField(default=True)
    friend_request_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f'Notification Settings for {self.user.username}'
