from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import youtube_validator
from users.models import User


class LessonSerializer(ModelSerializer):
    url = serializers.CharField(validators=[youtube_validator])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField(read_only=True)
    lesson_list = LessonSerializer(source="lesson", many=True, read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_quantity_lessons(self, obj):
        return obj.lesson.filter(course=obj).count()

    def get_subscription(self, odj):
        user = User.objects.get(is_active=True)
        if odj.subscription.filter(owner=user).count() < 1:
            return "нет подписки"
        return "есть подписка"


class CourseDitailSerializer(serializers.ModelSerializer):
    number_lessons = serializers.SerializerMethodField(read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    def get_number_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription(self, odj):
        user = User.objects.get(is_active=True)
        if odj.subscription.filter(owner=user).count() < 1:
            return "нет подписки"
        return "есть подписка"

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'number_lessons', 'subscription', 'owner']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
