from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from protected_media.models import ProtectedImageField


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
    user_type = models.CharField(max_length=20, choices=UserTypes.choices(), default=UserTypes.free, )
    blocked = models.BooleanField(default=False)
    firebase_user_id = models.CharField(max_length=200, null=True, blank=True)
    fcm_token = models.CharField(max_length=255, null=True, blank=True)  # for push notifications

    # user data
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    description = models.TextField(verbose_name='Описание')
    photo = ProtectedImageField(upload_to='user_photos/', blank=True, null=True, verbose_name='Фото')
    photo_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на фото (Firebase)')

    # user social data
    friends = models.ManyToManyField("self", blank=True, verbose_name='Друзья')
    friendship_requests = models.ManyToManyField("self", blank=True, symmetrical=False,
                                                 related_name='pending_friend_requests',
                                                 verbose_name='Запросы в друзья')

    # App related stuff
    last_login_datetime = models.DateTimeField(auto_now=True, verbose_name='Последний вход')
    points = models.IntegerField(default=0, verbose_name='Баллы')
    day_streak = models.IntegerField(default=0, verbose_name='Дневная серия')
    max_day_streak = models.IntegerField(default=0, verbose_name='Максимальная дневная серия')

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.pk} Profile of {self.name}'

    def update_activity_date(self, register_login: bool):
        """
        Обновляет дату активности пользователя и дневную серию
        :param register_login: True - фиксируем вход пользователя, False - это обновление day_streak
        """
        today = timezone.now()
        last_active_day: UserActivityDateModel = self.activity_dates.last()

        if register_login:
            self.last_login_datetime = today
        else:
            # Если прошло меньше 5ти минут с последнего входа, то не обновляем активность
            if (today - self.last_login_datetime).minutes < 5:
                return

        if last_active_day is not None:
            difference = (today.date() - last_active_day.datetime.date()).days
            if difference == 0:
                return
            elif difference == 1 and not register_login:
                self.add_points(points=1, description='Бонус за дневную серию')
                self.day_streak += 1
                if self.day_streak > self.max_day_streak:
                    self.max_day_streak = self.day_streak
                self.save()

                if self.day_streak % 10 == 0:
                    self.add_points(points=5, description='Бонусы за 10 дней подряд')
            elif difference > 1:
                self.day_streak = 0
                self.save()

        if not register_login:
            self.activity_dates.create()

    def add_points(self, points: int, description: str):
        if points < 0:
            raise ValueError('Points must be positive')
        if description == '':
            raise ValueError('Description must be filled')
        self.points += points
        self.save()
        UserPointAddHistory.objects.create(user=self, points=points, description=description)

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


class UserActivityDateModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='activity_dates')
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Активность пользователя'
        verbose_name_plural = 'Активности пользователей'

    def __str__(self):
        return f'{self.pk} Activity of [{self.user}] on {self.date}'


class UserPointAddHistory(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='point_add_history')
    points = models.IntegerField()
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'История добавления баллов'
        verbose_name_plural = 'Истории добавления баллов'

    def __str__(self):
        return f'{self.pk} UserPointAddHistory'
