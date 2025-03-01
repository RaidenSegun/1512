from ckeditor.fields import RichTextField
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):

    def validate_phone_number(value):
        pattern = r'^\+996\d{9}$'
        if not re.match(pattern, value):
            raise ValidationError("Номер телефона должен быть в формате +996XXXXXXXXX")

    phone_number = models.CharField(
        max_length=13,
        unique=True,
        help_text="Формат: +996XXXXXXXXX",
        verbose_name="Номер телефона",
        validators=[validate_phone_number]
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Возраст"
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        

    
class Todo(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Заголовок"
    )

    description = RichTextField(
        verbose_name="Описание"
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name="Завершено"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
        )
    
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        verbose_name="Изображение"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"