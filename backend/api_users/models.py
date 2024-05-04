from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', blank=True)
    friends = models.ManyToManyField("self", blank=True)
    friendship_requests = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name='requests_sent')
    firebase_user_id = models.CharField(max_length=200, null=True, blank=True)

    # Firebase Cloud Messaging token for push notifications
    fcm_token = models.CharField(max_length=255, null=True, blank=True)
    blocked = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return f'Profile of {self.name}'

    def send_friend_request(self, to_user):
        if (to_user != self) and (to_user not in self.friends.all()):
            to_user.friendship_requests.add(self)

    def accept_friend_request(self, from_user):
        if from_user in self.friendship_requests.all():
            self.friendship_requests.remove(from_user)
            self.friends.add(from_user)
            from_user.friends.add(self)

    def decline_friend_request(self, from_user):
        if from_user in self.friendship_requests.all():
            self.friendship_requests.remove(from_user)


class NotificationSettings(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    periodic_lesson_reminders = models.BooleanField(default=True)
    friend_request_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f'Notification Settings for {self.user.username}'
