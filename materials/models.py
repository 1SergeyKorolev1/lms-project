from django.db import models

from config import settings
from config.settings import AUTH_USER_MODEL

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Название", help_text="Введите название курса"
    )
    preview = models.ImageField(
        upload_to="materials/img", verbose_name="Превью", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="владелец",
        help_text="Укажите владельца",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Название", help_text="Введите название урока"
    )
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    preview = models.ImageField(
        upload_to="materials/", verbose_name="Превью", **NULLABLE
    )
    url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="lesson",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="владелец",
        help_text="Укажите владельца",
        **NULLABLE,
    )

    def __str__(self):
        return f"Урок{self.name}, курс {self.course}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

class Subscription(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", **NULLABLE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="subscription", **NULLABLE
    )

    def __str__(self):
        return f"Подписка на {self.course.name}."

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
