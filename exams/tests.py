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

        self.subject = Subject.objects.create(title='Maths')

        self.teacher_user = User.objects.create(username='teacher', password='123456')
        self.teacher = Teacher.objects.create(user=self.teacher_user, subject=self.subject)

        self.student_user = User.objects.create(username='test', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.student_user, clazz=self.clazz)

        self.exam = Exam.objects.create(
            subject=self.subject,
            date=datetime.strptime('Jun 2 2020 1:50PM', '%b %d %Y %I:%M%p').date(),
            clazz=self.clazz,
            topic='Quadratic inequations',
            details='This will be the hardest **** ever!!!',
            author=self.teacher
        )

    def test_exams_list_with_anonymous_user(self):
        request = self.client.get(reverse(self.list_view_name))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_exams_detail_with_anonymous_user(self):
        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id})
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_exams_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(reverse(self.list_view_name))

        self.assertEqual(
            self.subject.title, request.data[0]['subject']['title']
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_exams_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id})
        )

        self.assertIsNotNone(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_exams_list_with_expired_date(self):
        self.client.force_authenticate(user=self.student_user)
        self.exam.date = datetime.strptime('Jun 2 2000 1:50PM', '%b %d %Y %I:%M%p').date()
        self.exam.save()

        request = self.client.get(reverse(self.list_view_name))

        self.assertEqual(request.data, [])
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_exams_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id + 1})
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_exams_detail_with_valid_id(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id})
        )

        self.assertEqual(request.data['details'], self.exam.details)
        self.assertEqual(request.data['topic'], self.exam.topic)
        self.assertEqual(request.data['subject']['title'], self.subject.title)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_exams_creation_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.exam.topic = 'glucimir'
        post_data = self.serializer_class(self.exam).data

        request = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_creation_with_empty_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam.topic = ''
        post_data = self.serializer_class(self.exam).data

        request = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(request.data['topic'], ['This field may not be blank.'])
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exams_creation_with_too_long_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam.topic = 'glucimir' * 20
        post_data = self.serializer_class(self.exam).data

        request = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(
            request.data['topic'],
            ['Ensure this field has no more than 60 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exams_creation_with_valid_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam.topic = 'glucimir'
        post_data = self.serializer_class(self.exam).data

        request = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_exams_update_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.exam.topic = 'glucimir'
        put_data = self.serializer_class(self.exam).data

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_update_with_empty_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam.topic = ''
        put_data = self.serializer_class(self.exam).data

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id}),
            put_data,
            format='json'
        )

        self.assertEqual(request.data['topic'], ['This field may not be blank.'])
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exams_update_with_too_long_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam.topic = 'glucimir' * 20
        put_data = self.serializer_class(self.exam).data

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['topic'],
            ['Ensure this field has no more than 60 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exams_update_with_valid_topic(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.exam.topic = 'glucimir'
        put_data = self.serializer_class(self.exam).data

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id}),
            put_data,
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_exams_update_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject)
        self.exam.author = new_teacher
        self.exam.save()

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id}),
            {'topic': 'HAHAHA I AM ANONYMOUS!'},
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject)
        self.exam.author = new_teacher
        self.exam.save()

        request = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id})
        )

        self.assertEqual(
            request.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_deletion(self):
        self.client.force_authenticate(user=self.teacher_user)

        request = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.exam.id})
        )

        self.assertEqual(
            request.data['message'], 'Exam successfully deleted.'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
