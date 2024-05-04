from django.db import models
from api_users.models import UserModel


class UserTasksProfile(models.Model):
    user_profile = models.OneToOneField(UserModel, on_delete=models.CASCADE, verbose_name='Профиль пользователя',
                                        related_name='tasks_profile')
    completed_quizzes = models.ManyToManyField('QuizBatch', related_name='completed_users',
                                               verbose_name='Пройденные викторины')
    survey_completed = models.BooleanField(
        default=False, verbose_name='Опрос пройден')
    earned_coins = models.IntegerField(
        default=0, verbose_name='Заработанные монеты c задании')
    curr_streak = models.IntegerField(
        default=0, verbose_name='Нынешняя серия правильных ответов')
    max_streak = models.IntegerField(
        default=0, verbose_name='Максимальная серия правильных ответов')

    def __str__(self):
        return f'{self.id} Пользователь Задании [{self.user_profile}]'

    class Meta:
        verbose_name = 'Пользователь Задании'
        verbose_name_plural = 'Пользователи Задании'

    def add_coins(self, coins: int):
        self.earned_coins += coins
        self.user_profile.add_xp_and_coins(coins=coins)
        self.save()

    def correct_answer(self):
        self.curr_streak += 1

        coins = 5
        if self.curr_streak % 3 == 0 and self.curr_streak != 0:
            coins += 1
        self.add_coins(coins)

        if self.curr_streak > self.max_streak:
            self.max_streak = self.curr_streak
        self.save()
        return coins

    def incorrect_answer(self):
        self.curr_streak = 0
        self.save()


# ---------------------- Quizzes ----------------------
class QuizBatch(models.Model):
    CARD_COLOR_CHOICES = [
        ('blue', 'Синий'),
        ('green', 'Зеленый'),
    ]
    name = models.CharField(max_length=2000, verbose_name='Название')
    card_color = models.CharField(
        max_length=100, choices=CARD_COLOR_CHOICES, verbose_name='Цвет карточки')

    def __str__(self):
        return f'{self.id} Викторина [{self.name}]'

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'


class QuizQuestion(models.Model):
    quiz_batch = models.ForeignKey(QuizBatch, on_delete=models.CASCADE, verbose_name='Викторина',
                                   related_name='questions')
    question = models.CharField(max_length=100, verbose_name='Вопрос')

    def __str__(self):
        return f'{self.id} Вопрос викторины'

    class Meta:
        verbose_name = 'Вопрос викторины'
        verbose_name_plural = 'Вопросы викторины'


class QuizQuestionAnswer(models.Model):
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, verbose_name='Вопрос',
                                      related_name='answers')
    answer = models.CharField(max_length=2000, verbose_name='Ответ')
    is_correct = models.BooleanField(
        default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return f'{self.id} Ответ Викторины'

    class Meta:
        verbose_name = 'Ответ на вопрос викторины'
        verbose_name_plural = 'Ответы на вопросы викторины'


class UserQuizQuestion(models.Model):
    user_tasks_profile = models.ForeignKey(UserTasksProfile, on_delete=models.CASCADE, verbose_name='Пользователь',
                                           related_name='quiz_questions')
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, verbose_name='Вопрос',
                                      related_name='user_answers')
    answer = models.ForeignKey(
        QuizQuestionAnswer, on_delete=models.CASCADE, verbose_name='Ответ')
    coins_earned = models.IntegerField(
        default=0, verbose_name='Заработанные монеты')

    def __str__(self):
        return f'{self.id} Ответ на вопрос викторины'

    class Meta:
        verbose_name = 'Ответ на вопрос викторины'
        verbose_name_plural = 'Ответы на вопросы викторины'


# ---------------------- Surveys ----------------------
class SurveyQuestion(models.Model):
    question = models.CharField(max_length=2000, verbose_name='Вопрос')

    def __str__(self):
        return f'{self.id} Вопрос Опроса "{self.question}"'

    class Meta:
        verbose_name = 'Опрос: вопрос'
        verbose_name_plural = 'Опрос: вопросы'


class UserSurveyAnswer(models.Model):
    user_tasks_profile = models.ForeignKey(UserTasksProfile, on_delete=models.CASCADE, verbose_name='Пользователь',
                                           related_name='survey_answers')
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, verbose_name='Вопрос',
                                        related_name='answers')
    mark = models.IntegerField(
        verbose_name='Оценка', null=False, default=False)

    def __str__(self):
        return f'{self.id} Ответ опроса '

    class Meta:
        verbose_name = 'Опрос: ответ'
        verbose_name_plural = 'Опрос: ответы'

    def save(self, *args, **kwargs):
        if self.mark < 1 or self.mark > 10:
            raise ValueError('Оценка должна быть от 1 до 10')
        super().save(*args, **kwargs)
