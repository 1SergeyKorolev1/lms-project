from rest_framework.exceptions import ValidationError


def youtube_validator(value):
    if "youtube.com" not in value.lower():
        raise ValidationError("можно использовать ссылки только на youtube.com")
