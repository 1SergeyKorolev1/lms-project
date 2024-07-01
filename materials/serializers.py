from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lesson_list = LessonSerializer(source="lesson", many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_quantity_lessons(self, obj):
        return obj.lesson.filter(course=obj).count()


class CourseDitailSerializer(serializers.ModelSerializer):
    number_lessons = serializers.SerializerMethodField(read_only=True)

    def get_number_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'number_lessons']
