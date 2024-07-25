import re
from rest_framework.serializers import ValidationError


def validate_forbidden_words(value):
    """ проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com """
    if 'youtube.com' not in value.lower():
        raise ValidationError('Ссылку использовать нельзя')
