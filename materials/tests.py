from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from .serializers import MaterialSerializer
from .models import Material
from students.models import Class, Subject, Student, Teacher


class MaterialsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'materials:nested-materials-list'
        self.detail_view_name = 'materials:nested-materials-detail'
        self.serializer_class = MaterialSerializer

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='test_subject')

        self.student_user = User.objects.create(username='test', password='pass')
        self.student = Student.objects.create(user=self.student_user, clazz=self.clazz)

        self.teacher_user = User.objects.create(username='author', password='pass123')
        self.teacher = Teacher.objects.create(user=self.teacher_user, subject=self.subject)

        self.material = Material.objects.create(
            title='bla bla bla',
            section='Quadratic inequations',
            content='Here I will put some useful links for the current topic.',
            class_number=self.clazz.number,
            subject=self.subject,
            author=self.teacher
        )

    def test_materials_list_with_anonymous_user(self):
        request = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            )
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_materials_detail_with_anonymous_user(self):
        request = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            )
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_materials_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            )
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_materials_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.student_user)

        request = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            )
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_materials_creation_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.material.title = 'С0002ГР'
        post_data = self.serializer_class(self.material).data

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'You do not have permission to perform this action.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_materials_creation_with_too_short_title(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = '.'
        post_data = self.serializer_class(self.material).data

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            request.data['title'],
            ['Ensure this field has at least 3 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_too_long_title(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'Svetlosyanka' * 150
        post_data = self.serializer_class(self.material).data

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            request.data['title'],
            ['Ensure this field has no more than 150 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_too_short_section(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.section = '.'
        post_data = self.serializer_class(self.material).data

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            request.data['section'],
            ['Ensure this field has at least 3 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_too_long_section(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.section = 'Svetlosyanka' * 150
        post_data = self.serializer_class(self.material).data

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            request.data['section'],
            ['Ensure this field has no more than 150 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_blank_content(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.content = ''
        post_data = self.serializer_class(self.material).data

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            request.data['content'],
            ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_creation_with_valid_data(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'Hvala!'
        self.material.section = 'TBA'
        self.material.content = 'ELSYSER is damn good!'
        post_data = self.serializer_class(self.material).data

        request = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_materials_update_with_student_account(self):
        self.client.force_authenticate(user=self.student_user)
        self.material.title = 'С0002ГР'
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'You do not have permission to perform this action.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_materials_update_with_invalid_subject_id(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'Hvala!'
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id + 1,
                    'pk': self.material.id
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_materials_update_with_invalid_id(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'Hvala!'
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id + 1
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_materials_update_with_too_short_title(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = '.'
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['title'],
            ['Ensure this field has at least 3 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_too_long_title(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'Svetlosyanka' * 150
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['title'],
            ['Ensure this field has no more than 150 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_too_short_section(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.section = '.'
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['section'],
            ['Ensure this field has at least 3 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_too_long_section(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.section = 'Svetlosyanka' * 150
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['section'],
            ['Ensure this field has no more than 150 characters.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_blank_content(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.content = ''
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['content'],
            ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_materials_update_with_valid_data(self):
        self.client.force_authenticate(user=self.teacher_user)
        self.material.title = 'Hvala!'
        self.material.section = 'TBA'
        self.material.content = 'ELSYSER is damn good!'
        put_data = self.serializer_class(self.material).data

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
            put_data,
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_materials_update_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject)
        self.material.author = new_teacher
        self.material.save()

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
            {'topic': 'HAHAHA I AM ANONYMOUS!'},
            format='json'
        )

        self.assertEqual(
            request.data['message'], 'You can edit only your own materials.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_materials_deletion_with_invalid_subject_id(self):
        self.client.force_authenticate(user=self.teacher_user)

        request = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id + 1,
                    'pk': self.material.id
                }
            )
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_materials_deletion_with_invalid_id(self):
        self.client.force_authenticate(user=self.teacher_user)

        request = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id + 1
                }
            )
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_materials_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.teacher_user)

        new_user = User.objects.create(username='test2', password='pass')
        new_teacher = Teacher.objects.create(user=new_user, subject=self.subject)
        self.material.author = new_teacher
        self.material.save()

        request = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
        )

        self.assertEqual(
            request.data['message'], 'You can delete only your own materials.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_materials_deletion(self):
        self.client.force_authenticate(user=self.teacher_user)

        request = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'subject_pk': self.material.subject.id,
                    'pk': self.material.id
                }
            ),
        )

        self.assertEqual(
            request.data['message'], 'Material successfully deleted.'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
