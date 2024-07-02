from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from materials.models import Lesson, Course, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='tedt@tru.ru')
        self.course = Course.objects.create(name='test_name', owner=self.user)
        self.lesson = Lesson.objects.create(name='test_name', course=self.course, owner=self.user)
        self.subscription = Subscription.objects.create(owner=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.course.name
        )
        self.assertEqual(
            data.get('owner'), 1
        )
        self.assertEqual(
            data.get('number_lessons'), 1
        )
        self.assertEqual(
            data.get('subscription'), 'есть подписка'
        )

