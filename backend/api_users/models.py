from django.contrib.auth.models import AbstractUser
from django.db import models


class UserTypes:
    free = 'free'
    paid = 'paid'
    premium_paid = 'premium_paid'

    @classmethod
    def choices(cls):
        return [
            (cls.free, 'Бесплатный'),
            (cls.paid, 'Оплаченный'),
            (cls.premium_paid, 'Премиум оплаченный'),
        ]


class UserModel(AbstractUser):
    blocked = models.BooleanField(default=False)
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    photo_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на фото')
    friends = models.ManyToManyField("self", blank=True, verbose_name='Друзья')
    friendship_requests = models.ManyToManyField("self", blank=True, symmetrical=False,
                                                 related_name='pending_friend_requests',
                                                 verbose_name='Запросы в друзья')
    firebase_user_id = models.CharField(max_length=200, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=UserTypes.choices(), default=UserTypes.free, )
    # Firebase Cloud Messaging token for push notifications
    fcm_token = models.CharField(max_length=255, null=True, blank=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.pk} Profile of {self.name}'

    def is_paid(self):
        return self.user_type in (UserTypes.paid, UserTypes.premium_paid)

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
        return f'Настройки Уведомлении для пользователя {self.user.username}'
