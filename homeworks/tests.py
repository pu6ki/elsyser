from datetime import datetime, timedelta

from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from students.models import Class, Subject, Student, Teacher

from .serializers import HomeworkSerializer, SubmissionSerializer
from .models import Homework, Submission


class HomeworksViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'homeworks:homeworks-list'
        self.detail_view_name = 'homeworks:homeworks-detail'
        self.serializer_class = HomeworkSerializer

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='test_subject')

        self.student_user = User.objects.create(username='test', password='pass')
        self.teacher_user = User.objects.create(username='author', password='pass123')

        self.teacher = Teacher.objects.create(user=self.teacher_user, subject=self.subject)
        self.student = Student.objects.create(user=self.student_user, clazz=self.clazz)

        self.homework = Homework.objects.create(
            subject=self.subject,
            clazz=self.clazz,
            deadline=datetime.now().date(),
            details='something interesting',
            author=self.teacher
        )

    def test_homeworks_list_with_anonymous_user(self):
        request = self.client.get(reverse(self.list_view_name))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_homeworks_detail_with_anonymous_user(self):
        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id})
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_homeworks_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(reverse(self.list_view_name))

        self.assertIsNotNone(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_homeworks_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id})
        )

        self.assertEqual(
            request.data['clazz']['number'], self.student.clazz.number
        )
        self.assertEqual(
            request.data['clazz']['letter'], self.student.clazz.letter
        )
        self.assertEqual(request.data['details'], self.homework.details)
        self.assertEqual(request.data['subject']['title'], self.subject.title)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_homeworks_list_with_expired_date(self):
        self.client.force_authenticate(user=self.student_user)
        self.homework.deadline -= timedelta(days=5)
        self.homework.save()

        request = self.client.get(reverse(self.list_view_name))

        self.assertEqual(request.data, [])
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_homeworks_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id + 1})
        )

        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_homeworks_creation_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.homework.details = 'С0002ГР'
        post_data = self.serializer_class(self.homework).data

        request = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_homeworks_creation_with_too_long_details(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.homework.details = 'C0002ГР' * 256
        post_data = self.serializer_class(self.homework).data

        request = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            request.data['details'],
            ['Ensure this field has no more than 256 characters.']
        )

    def test_homeworks_creation_with_valid_details(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.homework.details = 'C0002ГР'
        post_data = self.serializer_class(self.homework).data

        request = self.client.post(
            reverse(self.list_view_name), post_data, format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_homeworks_update_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.homework.details = 'С0002ГР'
        put_data = self.serializer_class(self.homework).data

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_homeworks_update_with_too_long_details(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.homework.details = 'C0002ГР' * 256
        put_data = self.serializer_class(self.homework).data

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id}),
            put_data,
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            request.data['details'],
            ['Ensure this field has no more than 256 characters.']
        )

    def test_homeworks_update_with_valid_details(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.homework.details = 'C0002ГР'
        put_data = self.serializer_class(self.homework).data

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id}),
            put_data,
            format='json'
        )

        self.assertEqual(request.data['details'], self.homework.details)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_homeworks_update_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject)
        self.homework.author = new_teacher
        self.homework.save()

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id}),
            {'details': 'HAHAHA I AM ANONYMOUS!'},
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_homeworks_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject)
        self.homework.author = new_teacher
        self.homework.save()

        request = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id})
        )

        self.assertEqual(
            request.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_homeworks_deletion(self):
        self.client.force_authenticate(user=self.teacher_user)

        request = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.homework.id})
        )

        self.assertEqual(Homework.objects.count(), 0)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)


class SubmissionsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'homeworks:submissions-list'
        self.detail_view_name = 'homeworks:submissions-detail'
        self.serializer_class = SubmissionSerializer

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='test_subject')

        self.student_user1 = User.objects.create(username='test', password='pass')
        self.student_user2 = User.objects.create(username='test1', password='password')
        self.teacher_user = User.objects.create(username='author', password='pass123')

        self.teacher = Teacher.objects.create(user=self.teacher_user, subject=self.subject)
        self.student1 = Student.objects.create(user=self.student_user1, clazz=self.clazz)
        self.student2 = Student.objects.create(user=self.student_user2, clazz=self.clazz)

        self.homework = Homework.objects.create(
            subject=self.subject,
            clazz=self.clazz,
            deadline=datetime.now().date(),
            details='something interesting',
            author=self.teacher
        )

        self.student1_submission = Submission.objects.create(
            homework=self.homework,
            student=self.student1,
            content='this is my solution.'
        )
        self.student2_submission = Submission.objects.create(
            homework=self.homework,
            student=self.student2,
            content='noonecansaveyoufromwhatyouwant'
        )

    def test_submissions_list_with_anonymous_user(self):
        request = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id
                }
            )
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_submissions_detail_with_anonymous_user(self):
        request = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student1_submission.id
                }
            )
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_submissions_list_with_student_user(self):
        self.client.force_authenticate(user=self.student_user1)

        request = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id
                }
            )
        )

        self.assertNotEqual(
            request.data[0],
            SubmissionSerializer(self.student2_submission).data
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_submissions_detail_with_student_user(self):
        self.client.force_authenticate(user=self.student_user1)

        request = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student1_submission.id
                }
            )
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_submissions_detail_of_another_student(self):
        self.client.force_authenticate(user=self.student_user1)

        request = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student2_submission.id
                }
            )
        )

        self.assertEqual(
            request.data['detail'], 'You do not have permission to perform this action.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_submissions_list_with_teacher_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        request = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id
                }
            )
        )

        self.assertEqual(request.data[1]['id'], self.student1_submission.id)
        self.assertEqual(request.data[0]['id'], self.student2_submission.id)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_submissions_detail_with_teacher_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        request = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student1_submission.id
                }
            )
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_checked_submissions_list(self):
        self.client.force_authenticate(user=self.teacher_user)

        self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student1_submission.id
                }
            ),
            {'checked': True},
            format='json'
        )
        self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student2_submission.id
                }
            ),
            {'checked': True},
            format='json'
        )

        request = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id
                }
            )
        )

        self.assertEqual(request.data, [])
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_submission_creation_with_teacher_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id
                }
            ),
            {'content': 'test'},
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'Only students are allowed to view and modify this content.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_second_submission_creation(self):
        self.client.force_authenticate(user=self.student_user1)

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id
                }
            ),
            {'content': 'test'},
            format='json'
        )

        self.assertEqual(request.data['detail'], 'You can submit only one submission.')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_checked_submission_update(self):
        self.client.force_authenticate(user=self.teacher_user)

        self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student1_submission.id
                }
            ),
            {'checked': True},
            format='json'
        )

        self.client.force_authenticate(user=self.student_user1)

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student1_submission.id
                }
            ),
            {'content': 'testing'},
            format='json'
        )

        self.assertEqual(request.data['detail'], 'Submission is already checked.')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_submission_update(self):
        self.client.force_authenticate(user=self.student_user1)

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student1_submission.id
                }
            ),
            {'content': 'testing'},
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_submission_update_of_another_student(self):
        self.client.force_authenticate(user=self.student_user2)

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'homeworks_pk': self.homework.id,
                    'pk': self.student1_submission.id
                }
            ),
            {'content': 'testing'},
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'You do not have permission to perform this action.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
