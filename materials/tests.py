from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='tedt@tru.ru')
        self.course = Course.objects.create(name='test_name', owner=self.user)
        self.lesson = Lesson.objects.create(name='test_name', course=self.course, owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson_get', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.course.name
        )
        self.assertEqual(
            data.get('owner'), 4
        )
        self.assertEqual(
            data.get('course'), 4
        )

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')  # 'materials:course-list' у вьюсета курса
        data = {
            'name': 'test_name',
            'url': 'yes link youtube.com',
            'course': self.lesson.course.id
        }
        response = self.client.post(url, data)
        data_ = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            data_.get('url'), 'yes link youtube.com'
        )
        self.assertEqual(
            data_.get('name'), 'test_name'
        )
        self.assertEqual(
            data_.get('owner'), 2
        )
        self.assertEqual(
            data_.get('course'), 2
        )

    def test_lesson_update(self):
        url = reverse('materials:lesson_update', args=(self.lesson.pk,))  # 'materials:course-detail' у вьюсета курса
        data = {
            'name': 'test',
            'url': 'youtube.com',
        }
        response = self.client.patch(url, data)
        data_ = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data_.get('name'), 'test'
        )
        self.assertEqual(
            data_.get('url'), 'youtube.com'
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson_delete', args=(self.lesson.pk,))  # 'materials:course-detail' у вьюсета курса
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

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
