from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from datetime import datetime, timedelta

from .models import Class, Student, Subject, Exam, News


class RegisterViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_data = {
            'user': {
                'first_name': 'test',
                'last_name': 'user',
                'email': 'tester@gmail.com',
                'password': 'testerpassword123456',
            },
            'clazz': {
                'number': 10,
                'letter': 'A',
            },
        }


    def test_registration_with_empty_email(self):
        self.test_data['user']['email'] = ''

        request = self.client.post(
            reverse('students:register'), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['user']['email'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


    def test_registration_with_invalid_email(self):
        self.test_data['user']['email'] = 'tester'

        request = self.client.post(
            reverse('students:register'), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['user']['email'], ['Enter a valid email address.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


    def test_registration_with_empty_password(self):
        self.test_data['user']['password'] = ''

        request = self.client.post(
            reverse('students:register'), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['user']['password'], ['Password cannot be empty.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


    def test_registration_with_too_short_password(self):
        self.test_data['user']['password'] = 'test'

        request = self.client.post(
            reverse('students:register'), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['user']['password'], ['Password too short.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


    def test_registration_with_invalid_clazz(self):
        self.test_data['clazz']['number'] = 0

        request = self.client.post(
            reverse('students:register'), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['clazz']['number'], ['"0" is not a valid choice.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


    def test_registration_with_valid_data(self):
        request = self.client.post(
            reverse('students:register'), self.test_data, format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


class ProfileViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='test_user',
            first_name='test',
            last_name='user',
            email='tester@gmail.com',
            password='pass'
        )
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)


    def test_profile_with_anonymous_user(self):
        request = self.client.get(reverse('students:profile'))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_profile_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(reverse('students:profile'))

        self.assertNotIn('password', request.data['user'])
        self.assertEqual(self.student.user.username, request.data['user']['username'])
        self.assertEqual(self.student.clazz.number, request.data['clazz']['number'])
        self.assertEqual(self.student.clazz.letter, request.data['clazz']['letter'])
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class ExamsViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='test', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)
        self.subject = Subject.objects.create(title='test_subject')
        self.exam = Exam.objects.create(
            subject=self.subject,
            date=datetime.now().date(),
            clazz=self.clazz,
            topic='topic'
        )


    def test_exams_with_anonymous_user(self):
        request = self.client.get(reverse('students:exams'))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_exams_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(reverse('students:exams'))

        self.assertIn(self.subject.title, request.data[0]['subject']['title'])
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_exams_with_expired_date(self):
        self.client.force_authenticate(user=self.user)
        self.exam.date -= timedelta(days=5)
        self.exam.save()

        request = self.client.get(reverse('students:exams'))

        self.assertEqual(request.data, [])
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class NewsViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='test', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)
        self.news = News.objects.create(
            title='test_news', content='blablabla', clazz=self.clazz
        )


    def test_news_with_anonymous_user(self):
        request = self.client.get(reverse('students:news'))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_news_with_same_class(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(reverse('students:news'))

        self.assertIn(self.news.title, request.data[0]['title'])
        self.assertIn(self.news.content, request.data[0]['content'])
        self.assertIn(
            datetime.now().date().strftime('%Y-%m-%d'), request.data[0]['date']
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_news_with_different_class(self):
        self.client.force_authenticate(user=self.user)
        self.student.clazz = Class.objects.create(number=11, letter='V')

        request = self.client.get(reverse('students:news'))

        self.assertEqual(request.data, [])
        self.assertEqual(request.status_code, status.HTTP_200_OK)
