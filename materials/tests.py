from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from students.models import Class, Subject, Student, Teacher

from .serializers import MaterialSerializer
from .models import Material


class MaterialsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'materials:nested_materials-list'
        self.detail_view_name = 'materials:nested_materials-detail'
        self.serializer_class = MaterialSerializer

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='test_subject')

        self.student_user = User.objects.create(username='test', password='pass')
        self.student = Student.objects.create(user=self.student_user, clazz=self.clazz)

        self.teacher_user = User.objects.create(username='author', password='pass123')
        self.teacher = Teacher.objects.create(user=self.teacher_user, subject=self.subject)

        self.material = Material.objects.create(
            title='test material',
            section='test material section',
            content='test material content',
            class_number=self.clazz.number,
            subject=self.subject,
            author=self.teacher
        )

    def test_materials_list_with_anonymous_user(self):
        response = self.client.get(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id})
        )

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_materials_detail_with_anonymous_user(self):
        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            )
        )

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_materials_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_materials_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_materials_creation_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.material.title = 'test title'
        post_data = self.serializer_class(self.material).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id}),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_materials_creation_with_too_short_title(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = '.'
        post_data = self.serializer_class(self.material).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id}),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['title'], ['Ensure this field has at least 3 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_too_long_title(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'test title' * 150
        post_data = self.serializer_class(self.material).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id}),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['title'], ['Ensure this field has no more than 150 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_too_short_section(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.section = '.'
        post_data = self.serializer_class(self.material).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id}),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['section'],
            ['Ensure this field has at least 3 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_too_long_section(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.section = 'test title' * 150
        post_data = self.serializer_class(self.material).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id}),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['section'], ['Ensure this field has no more than 150 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_blank_content(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.content = ''
        post_data = self.serializer_class(self.material).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id}),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_valid_data(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'test title'
        self.material.section = 'test section'
        self.material.content = 'test content'
        post_data = self.serializer_class(self.material).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'subject_pk': self.material.subject.id}),
            post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_materials_update_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.material.title = 'test title'
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['detail'], 'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_materials_update_with_invalid_subject_id(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'test title'
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id + 1, 'pk': self.material.id}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_materials_update_with_invalid_id(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'test title'
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id + 1}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_materials_update_with_too_short_title(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = '.'
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(response.data['title'], ['Ensure this field has at least 3 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_too_long_title(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'test title' * 150
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['title'], ['Ensure this field has no more than 150 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_too_short_section(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.section = '.'
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(response.data['section'], ['Ensure this field has at least 3 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_too_long_section(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.section = 'test title' * 150
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['section'], ['Ensure this field has no more than 150 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_blank_content(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.content = ''
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_valid_data(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'test title'
        self.material.section = 'test section'
        self.material.content = 'test content'
        put_data = self.serializer_class(self.material).data

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
            put_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_materials_update_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject)
        self.material.author = new_teacher
        self.material.save()

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
            {'topic': 'test topic'},
            format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_materials_deletion_with_invalid_subject_id(self):
        self.client.force_authenticate(user=self.teacher_user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id + 1, 'pk': self.material.id}
            )
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_materials_deletion_with_invalid_id(self):
        self.client.force_authenticate(user=self.teacher_user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id + 1}
            )
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_materials_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject)
        self.material.author = new_teacher
        self.material.save()

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_materials_deletion(self):
        self.client.force_authenticate(user=self.teacher_user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'subject_pk': self.material.subject.id, 'pk': self.material.id}
            ),
        )

        self.assertEqual(Material.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
