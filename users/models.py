from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"null": True, "blank": True}

PAYMENT_METHOD_LIST = [("наличные", "наличные"), ("перевод", "перевод")]


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
    last_login = models.DateTimeField(auto_now=True, verbose_name="Время последнего посещения",
                                      **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    date_payment = models.DateField(verbose_name="дата оплаты", auto_now_add=True)
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="оплаченный курс", **NULLABLE
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="оплаченный урок", **NULLABLE
    )
    payment_amount = models.PositiveIntegerField(verbose_name="сумма оплаты")
    payment_method = models.CharField(
        max_length=100, verbose_name="способ оплаты", choices=PAYMENT_METHOD_LIST
    )
    payment_link = models.URLField(max_length=400, verbose_name="ссылка на оплату", **NULLABLE)
    id_session = models.CharField(max_length=300, verbose_name="id сессии", **NULLABLE)

    def __str__(self):
        return f'{self.user}-{self.date_payment}, {self.payment_amount}-{self.payment_method}'

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплата"
