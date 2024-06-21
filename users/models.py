from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"null": True, "blank": True}

payment_method_list = {
    "наличными": "наличными",
    "переводом": "переводом"
}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35, verbose_name="Телефон", help_text="Укажите телефон", **NULLABLE
    )
    city = models.CharField(max_length=150, verbose_name="Город", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Пользователь', **NULLABLE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты'),
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE)
    payment_sum = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, choices=payment_method_list, verbose_name='Способ оплаты')

    def __str__(self):
        return (f'{self.user}: {self.payment_date}\n{self.payment_sum}, {self.payment_method}\n '
                f'за {self.paid_lesson} {self.paid_course}')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
