from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from django.db import models
import urllib.parse


class CustomUser(AbstractUser):
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'

    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Студент'),
        (ROLE_TEACHER, 'Преподаватель'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT,
        validators=[MaxLengthValidator(10)]
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Schedule(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название предмета')
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Начало занятия')
    end_time = models.TimeField(verbose_name='Конец занятия')
    location = models.CharField(max_length=200, blank=True, verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    teacher = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='schedules',
                                verbose_name='Преподаватель')

    def __str__(self):
        return f"{self.title} on {self.date} from {self.start_time} to {self.end_time}"

    def get_yandex_calendar_url(self):
        base_url = "https://calendar.yandex.com/?event"
        params = {
            'name': self.title,
            'description': self.description,
            'location': self.location,
            'start_time': f"{self.date}T{self.start_time}",
            'end_time': f"{self.date}T{self.end_time}"
        }
        return f"{base_url}&{urllib.parse.urlencode(params)}"