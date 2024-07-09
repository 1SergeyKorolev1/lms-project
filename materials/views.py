from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, generics

from materials.models import Course, Lesson, Subscription
from materials.paginations import MaterialsPagination
from materials.serializers import (CourseDitailSerializer, CourseSerializer,
                                   LessonSerializer, SubscriptionSerializer)
from materials.tasks import update_message
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDitailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        update_message.delay(instance.pk)
        return instance


class SubscriptionViewSet(APIView):

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course)

        subscription, created = Subscription.objects.get_or_create(owner=user, course=course_item)
        if not created:
            subscription.delete()
            message = 'Subscription removed'
        else:
            message = 'Subscription added'

        return Response({"message": message}, status=status.HTTP_201_CREATED)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialsPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)
