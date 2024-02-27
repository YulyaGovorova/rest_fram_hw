from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


from main.models import Course, Lesson, Subscription
from users.models import User


class InitialTestCase(APITestCase):

    def setUp(self):
        """Создание тестового пользователя, курса и урока"""
        self.client = APIClient()
        self.user = User.objects.create(email='user@gmail.com', password='123')
        # access_token = str(RefreshToken.for_user(self.user).access_token)
        # self.client.credentials(HTTP_AUTHORIZATION=F'Bearer {access_token}')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='test_course',
            description='test_course',
            owner=self.user,
            preview=None
        )

        self.lesson = Lesson.objects.create(
            name='test_lesson',
            description='test_lesson',
            course=self.course,
            video='http://www.youtube.com/test_lesson',
            owner=self.user,
            preview=None
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )


class LessonTestCase(InitialTestCase):

    def test_create(self):
        """Тестирование создания урока"""
        data = {
            'name': 'test_lesson_2',
            'description': 'test_lesson_2',
            'course': self.course.id,
            'video': 'http://www.youtube.com/test_lesson_2',
            'owner': self.user.id
        }

        response = self.client.post(reverse('main:lesson_create'), data=data)

        # print(response.status_code)
        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id + 1,
             'name': 'test_lesson_2',
             'preview': None,
             'description': 'test_lesson_2',
             'course': self.course.id,
             'owner': self.user.id,
             'video': 'http://www.youtube.com/test_lesson_2'
             }

        )

    def test_list(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(reverse('main:lesson_list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                 {'id': self.lesson.id,
                  'name': self.lesson.name,
                  'preview': None,
                  'description': self.lesson.description,
                  'course': self.course.id,
                  'owner': self.user.id,
                  'video': self.lesson.video
                  }
             ]
             }
        )

    def test_retrieve(self):
        """Тестирование вывода одного урока"""
        response = self.client.get(reverse('main:lesson_retrieve', kwargs={'pk': self.lesson.id}))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id,
             'name': self.lesson.name,
             'preview': None,
             'description': self.lesson.description,
             'course': self.course.id,
             'owner': self.user.id,
             'video': self.lesson.video
             }
        )

    def test_update(self):
        """Тестирование изменения урока"""
        data = {
            'name': 'test_lesson_update'
        }

        response = self.client.patch(
            reverse('main:lesson_update', kwargs={'pk': self.lesson.id}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id,
             'name': 'test_lesson_update',
             'preview': None,
             'description': self.lesson.description,
             'course': self.course.id,
             'owner': self.user.id,
             'video': self.lesson.video
             }
        )

    def test_delete(self):
        """Тестирование удаления урока"""
        response = self.client.delete(
            reverse('main:lesson_destroy', kwargs={'pk': self.lesson.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(InitialTestCase):

    def test_create(self):
        """Тестирование создания подписки"""

        data = {
            "user": self.user.id,
            "course": self.course.id
        }

        response = self.client.post(
            reverse("main:subscription_create", kwargs={'course_pk': self.course.id}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete(self):
        """Тестирование удаления подписки"""

        response = self.client.delete(
            reverse('main:subscription_delete', kwargs={'pk': self.subscription.id, })
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class CourseTestCase(InitialTestCase):

    def test_create(self):
        """Тестирование создания курса"""
        data = {
            'name': 'test_course_2',
            'description': 'test_course_2',
            'owner': self.user.id
        }

        response = self.client.post('/main/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2,
             'name': 'test_course_2',
             'subscribed': False,
             'preview': None,
             'lessons': [],
             'lessons_count': 0,
             'description': 'test_course_2',
             'owner': self.user.id,
             }

        )

    def test_list(self):
        """Тестирование вывода списка курсов"""
        response = self.client.get('/main/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [{
                 'id': 3,
                 'subscribed': True,
                 'lessons_count': 1,
                 'lessons': [{
                     'id': 2,
                     'name': 'test_lesson',
                     'preview': None,
                     'description': 'test_lesson',
                     'video': 'http://www.youtube.com/test_lesson',
                     'course': 3,
                     'owner': 2
                 }],
                 'name': 'test_course',
                 'preview': None,
                 'description': 'test_course',
                 'owner': 2}]
             }
        )

    def test_retrieve(self):
        """Тестирование вывода одного курса"""

        response = self.client.get('/main/', kwargs={'pk': self.course.id})

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [{
                    'id': 4,
                    'subscribed': True,
                    'lessons_count': 1,
                    'lessons': [{
                        'id': 3,
                        'name': 'test_lesson',
                        'preview': None,
                        'description': 'test_lesson',
                        'video': 'http://www.youtube.com/test_lesson',
                        'course': 4,
                        'owner': 3
                    }],
                    'name': 'test_course',
                    'preview': None,
                    'description': 'test_course',
                    'owner': 3
                }]
            }
        )

