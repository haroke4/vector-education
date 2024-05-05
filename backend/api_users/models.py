from django.db import models
from firebase_admin import auth


class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', blank=True)
    friends = models.ManyToManyField("self", blank=True)
    friendship_requests = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name='requests_sent')
    firebase_user_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def send_friendship_request(self, to_user):
        if (to_user != self) and (to_user not in self.friends.all()):
            to_user.friendship_requests.add(self)

    def accept_friendship_request(self, from_user):
        if from_user in self.friendship_requests.all():
            self.friendship_requests.remove(from_user)
            self.friends.add(from_user)
            from_user.friends.add(self)

    def decline_friendship_request(self, from_user):
        if from_user in self.friendship_requests.all():
            self.friendship_requests.remove(from_user)

    @classmethod
    def get_user_by_token(cls, token: str):
        try:
            decoded_token = auth.verify_id_token(token)
            firebase_user_id = decoded_token['uid']
        except ValueError:
            return None

        user = UserProfile.objects.get(firebase_user_id=firebase_user_id)
        return user


class NotificationSettings(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    periodic_lesson_reminders = models.BooleanField(default=True)
    friend_request_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f'Notification Settings for {self.user.name}'
