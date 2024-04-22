from django.db import models


class LessonCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    topic = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='lesson_videos', blank=True)
    lesson_number = models.PositiveIntegerField(blank=True, null=True)
    category = models.ForeignKey(LessonCategory, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.lesson_number is None or self.lesson_number > Lesson.objects.count() + 1:
            self.lesson_number = Lesson.objects.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic
