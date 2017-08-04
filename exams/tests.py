from datetime import datetime

from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from students.models import Class, Subject, Teacher, Student

from .serializers import ExamSerializer
from .models import Exam


class ExamsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'exams:exams-list'
        self.detail_view_name = 'exams:exams-detail'
        self.serializer_class = ExamSerializer

        self.subject1 = Subject.objects.create(title='Maths')
        self.subject2 = Subject.objects.create(title='Bulgarian Language')

        self.teacher_user = User.objects.create(username='teacher', password='123456')
        self.teacher = Teacher.objects.create(user=self.teacher_user, subject=self.subject1)

        self.student_user = User.objects.create(username='test', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.student_user, clazz=self.clazz)

        self.date = datetime.strptime('Jun 2 2020 1:50PM', '%b %d %Y %I:%M%p').date()

        self.exam1 = Exam.objects.create(
            subject=self.subject1,
            date=self.date,
            clazz=self.clazz,
            topic='Quadratic inequations',
            details='This will be the hardest **** ever!!!',
            author=self.teacher
        )
        self.exam2 = Exam.objects.create(
            subject=self.subject2,
            date=self.date,
            clazz=self.clazz,
            topic='Realism',
            details='idk idk dik',
            author=self.teacher
        )

    def test_exams_list_with_anonymous_user(self):
        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_exams_detail_with_anonymous_user(self):
        response = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id})
        )

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_exams_list_with_student_user(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(
            self.subject1.title, response.data[1]['subject']['title']
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exams_list_with_teacher_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.exam1.id)

    def test_exams_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id})
        )

        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exams_list_with_expired_date(self):
        self.client.force_authenticate(user=self.student_user)

        new_date = datetime.strptime('Jun 2 2000 1:50PM', '%b %d %Y %I:%M%p').date()
        self.exam1.date = new_date
        self.exam1.save()

        self.exam2.date = new_date
        self.exam2.save()

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exams_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.exam2.id + 1})
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_exams_detail_with_valid_id(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id})
        )

        self.assertEqual(response.data['details'], self.exam1.details)
        self.assertEqual(response.data['topic'], self.exam1.topic)
        self.assertEqual(response.data['subject']['title'], self.subject1.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exams_creation_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.exam1.topic = 'glucimir'
        post_data = self.serializer_class(self.exam1).data

        response = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_creation_with_empty_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam1.topic = ''
        post_data = self.serializer_class(self.exam1).data

        response = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(response.data['topic'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exams_creation_with_too_long_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam1.topic = 'glucimir' * 20
        post_data = self.serializer_class(self.exam1).data

        response = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(
            response.data['topic'],
            ['Ensure this field has no more than 60 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exams_creation_with_valid_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam1.topic = 'glucimir'
        post_data = self.serializer_class(self.exam1).data

        response = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_exams_update_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.exam1.topic = 'glucimir'
        put_data = self.serializer_class(self.exam1).data

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_update_with_empty_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam1.topic = ''
        put_data = self.serializer_class(self.exam1).data

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(response.data['topic'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exams_update_with_too_long_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam1.topic = 'glucimir' * 20
        put_data = self.serializer_class(self.exam1).data

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['topic'],
            ['Ensure this field has no more than 60 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exams_update_with_valid_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam1.topic = 'glucimir'
        put_data = self.serializer_class(self.exam1).data

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['topic'], self.exam1.topic)

    def test_exams_update_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject1)
        self.exam1.author = new_teacher
        self.exam1.save()

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id}),
            {'topic': 'HAHAHA I AM ANONYMOUS!'},
            format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject1)
        self.exam1.author = new_teacher
        self.exam1.save()

        response = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id})
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_deletion(self):
        self.client.force_authenticate(user=self.teacher_user)

        response = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.exam1.id})
        )

        self.assertEqual(Exam.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
