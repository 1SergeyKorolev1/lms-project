from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from materials.models import Course, Lesson, Subscription
from materials.validators import validate_forbidden_words


class LessonSerializer(ModelSerializer):
    url = serializers.CharField(validators=[validate_forbidden_words])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lesson_list = LessonSerializer(source="lesson", many=True, read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    def get_quantity_lessons(self, obj):
        return obj.lesson.filter(course=obj).count()

    def get_subscription(self, odj):
        user = self.context.get('request').user
        if odj.subscription.filter(user=user).count() < 1:
            return "нет подписки"
        return "есть подписка"

    class Meta:
        model = Course
        fields = "__all__"


class CourseDitailSerializer(serializers.ModelSerializer):
    number_lessons = serializers.SerializerMethodField(read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    def get_number_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription(self, odj):
        user = self.context.get('request').user
        if odj.subscription.filter(user=user).count() < 1:
            return "нет подписки"
        return "есть подписка"

    # def get_subscription(self, course):
    #     user = self.context.get('request').user
    #     course = self.context.get('view').kwargs.get('pk')
    #     subscription = Subscription.objects.filter(user=user, course=course)
    #     if subscription.exists():
    #         return "есть подписка"
    #     else:
    #         return "нет подписки"

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'number_lessons', 'subscription', 'owner']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
