from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Class, Subject, Student, Teacher, Grade
from .serializers import StudentProfileSerializer


class RegisterViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:register'

        self.test_data = {
            'user': {
                'username': 'tester',
                'first_name': 'test',
                'last_name': 'user',
                'email': 'tester@gmail.com',
                'password': 'testerpassword123456',
            },
            'clazz': {
                'number': 10,
                'letter': 'A',
            }
        }

    def test_registration_with_empty_email(self):
        self.test_data['user']['email'] = ''

        request = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['user']['email'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_email(self):
        self.test_data['user']['email'] = 'tester'

        request = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['user']['email'], ['Enter a valid email address.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_empty_password(self):
        self.test_data['user']['password'] = ''

        request = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['user']['password'], ['Password cannot be empty.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_too_short_password(self):
        self.test_data['user']['password'] = 'test'

        request = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['user']['password'], ['Password too short.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_clazz(self):
        self.test_data['clazz']['number'] = 0

        request = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            request.data['clazz']['number'], ['"0" is not a valid choice.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_valid_data(self):
        request = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        user_data = request.data['user']
        user = User.objects.get(**user_data)

        self.assertEqual(self.test_data['user']['username'], user.username)
        self.assertEqual(self.test_data['user']['first_name'], user.first_name)
        self.assertEqual(self.test_data['user']['last_name'], user.last_name)
        self.assertEqual(self.test_data['user']['email'], user.email)
        self.assertIsNotNone(
            Token.objects.get(user__username=user_data['username'])
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:login'

        self.user_data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': ''.join(map(str, range(1, 10)))
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        self.post_data = {
            'email_or_username': '',
            'password': self.user_data['password'],
        }

    def test_login_with_blank_email_or_username(self):
        request = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(
            request.data['email_or_username'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_blank_password(self):
        self.post_data['email_or_username'] = self.user.email
        self.post_data['password'] = ''

        request = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(
            request.data['password'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_email_or_username(self):
        self.post_data['email_or_username'] = 'invalid'

        request = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(
            request.data['non_field_errors'],
            ['Unable to log in with provided credentials.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_password(self):
        self.post_data['email_or_username'] = self.user.email
        self.post_data['password'] = 'invalidpassword'

        request = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(
            request.data['non_field_errors'],
            ['Unable to log in with provided credentials.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_valid_email_and_password(self):
        self.post_data['email_or_username'] = self.user.email

        request = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(self.token.key, request.data['token'])
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_login_with_valid_username_and_password(self):
        self.post_data['email_or_username'] = self.user.username

        request = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(self.token.key, request.data['token'])
        self.assertEqual(request.status_code, status.HTTP_200_OK)

class ProfileViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:profile-detail'

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='Maths')

        self.user1 = User.objects.create(
            username='tester',
            first_name='test',
            last_name='user',
            email='tester@gmail.com',
            password='pass'
        )
        self.user2 = User.objects.create(
            username='test',
            first_name='tester',
            last_name='user',
            email='test@gmail.com',
            password='password123456'
        )
        self.user3 = User.objects.create(
            username='teacher',
            first_name='teacher',
            last_name='user',
            email='test_teacher@gmail.com',
            password='123120382190'
        )

        self.student1 = Student.objects.create(
            user=self.user1,
            clazz=self.clazz,
            info='I am the lord of the rings.',
            profile_image_url='http://www.shockmansion.com/wp-content/myimages/2016/03/rr231.jpg'
        )
        self.student2 = Student.objects.create(
            user=self.user2, clazz=self.clazz, info='I am a starboy.'
        )
        self.teacher = Teacher.objects.create(
            user=self.user3, subject=self.subject, info='Your maths teacher.'
        )

    def test_profile_with_anonymous_user(self):
        request = self.client.get(
            reverse(self.view_name, kwargs={'pk': self.user1.id})
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_with_own_user(self):
        self.client.force_authenticate(user=self.user1)

        request = self.client.get(
            reverse(self.view_name, kwargs={'pk': self.user1.id})
        )

        self.assertEqual(
            self.student1.user.username, request.data['user']['username']
        )
        self.assertEqual(
            self.student1.clazz.number, request.data['clazz']['number']
        )
        self.assertEqual(
            self.student1.clazz.letter, request.data['clazz']['letter']
        )
        self.assertEqual(self.student1.info, request.data['info'])
        self.assertTrue(request.data['can_edit'])
        self.assertNotIn('password', request.data['user'])
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_profile_with_other_user(self):
        self.client.force_authenticate(user=self.user2)

        request = self.client.get(
            reverse(self.view_name, kwargs={'pk': self.user1.id})
        )

        self.assertEqual(
            self.student1.user.username, request.data['user']['username']
        )
        self.assertEqual(
            self.student1.clazz.number, request.data['clazz']['number']
        )
        self.assertEqual(
            self.student1.clazz.letter, request.data['clazz']['letter']
        )
        self.assertEqual(self.student1.info, request.data['info'])
        self.assertFalse(request.data['can_edit'])
        self.assertNotIn('password', request.data['user'])
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_profile_update_of_another_user(self):
        self.client.force_authenticate(user=self.user2)
        self.student1.user.username = 'MyNewUsername'
        self.student1.user.first_name = 'John'
        self.student1.user.last_name = 'Travolta'
        put_data = StudentProfileSerializer(self.student1).data

        request = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'You do not have permission to perform this action.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_update_with_invalid_username(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.user.username = ''
        put_data = StudentProfileSerializer(self.student1).data

        request = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['user']['username'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_invalid_first_name(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.user.first_name = ''
        put_data = StudentProfileSerializer(self.student1).data

        request = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['user']['first_name'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_invalid_last_name(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.user.last_name = ''
        put_data = StudentProfileSerializer(self.student1).data

        request = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['user']['last_name'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_invalid_profile_picture_url(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.profile_image_url = 'https://www.youtube.com/watch?v=vSoUp-SxLrQ'
        put_data = StudentProfileSerializer(self.student1).data

        request = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            request.data['profile_image_url'], ['URL is not a picture.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_valid_data(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.user.username = 'MyNewUsername'
        self.student1.user.first_name = 'John'
        self.student1.user.last_name = 'Travolta'
        self.student1.profile_image_url = 'http://books.sulla.bg/wp-content/uploads/2011/11/kurt_vonnegut.jpg'
        put_data = StudentProfileSerializer(self.student1).data

        request = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)

class GradesListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:grades-list'

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='Maths')

        self.user = User.objects.create(
            username='tester',
            first_name='test',
            last_name='user',
            email='tester@gmail.com',
            password='pass'
        )

        self.student = Student.objects.create(
            user=self.user,
            clazz=self.clazz,
            info='I am the lord of the rings.',
            profile_image_url='http://www.shockmansion.com/wp-content/myimages/2016/03/rr231.jpg'
        )

        self.grade1 = Grade.objects.create(
            value=5.67,
            subject=self.subject,
            student=self.student
        )
        self.grade2 = Grade.objects.create(
            value=4.82,
            subject=self.subject,
            student=self.student
        )

    def test_list_with_anonymous_user(self):
        request = self.client.get(
            reverse(self.view_name, kwargs={'subject_pk': self.subject.id})
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(
            reverse(self.view_name, kwargs={'subject_pk': self.subject.id})
        )

        self.assertEqual(request.data[0]['value'], self.grade2.value)
        self.assertEqual(request.data[1]['value'], self.grade1.value)
        self.assertEqual(
            request.data[0]['student']['user']['username'],
            self.user.username
        )
        self.assertEqual(
            request.data[1]['student']['user']['username'],
            self.user.username
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_list_with_invalid_subject_id(self):
        self.client.force_authenticate(user=self.user)
        request = self.client.get(
            reverse(self.view_name, kwargs={'subject_pk': self.subject.id - 1})
        )

        self.assertFalse(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

class GradesDetailViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:grades-detail'

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject1 = Subject.objects.create(title='Maths')
        self.subject2 = Subject.objects.create(title='Literature')

        self.user1 = User.objects.create(
            username='tester',
            first_name='test',
            last_name='user',
            email='tester@gmail.com',
            password='pass'
        )
        self.user2 = User.objects.create(
            username='tester1',
            first_name='test1',
            last_name='user1',
            email='tester@abv.bg',
            password='password123'
        )
        self.user3 = User.objects.create(
            username='tester2',
            first_name='test2',
            last_name='user2',
            email='tester@abv.com',
            password='password123456'
        )

        self.student1 = Student.objects.create(
            user=self.user1,
            clazz=self.clazz,
            info='I am the lord of the rings.',
            profile_image_url='http://www.shockmansion.com/wp-content/myimages/2016/03/rr231.jpg'
        )
        self.student2 = Student.objects.create(
            user=self.user2,
            clazz=self.clazz,
            info='information'
        )

        self.teacher = Teacher.objects.create(
            user=self.user3,
            subject=self.subject1
        )

        self.grade1 = Grade.objects.create(
            value=5.67,
            subject=self.subject1,
            student=self.student1
        )
        self.grade2 = Grade.objects.create(
            value=4.82,
            subject=self.subject1,
            student=self.student2
        )

    def test_grade_detail_with_anonymous_user(self):
        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            )
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_grade_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user1)

        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            )
        )

        self.assertEqual(request.data[0]['value'], self.grade1.value)
        self.assertEqual(
            request.data[0]['student']['user']['username'],
            self.user1.username
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_grade_detail_of_another_user(self):
        self.client.force_authenticate(user=self.user2)

        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            )
        )

        self.assertEqual(
            request.data['message'],
            'You can view only your own grades.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_grade_detail_with_non_graded_subject(self):
        self.client.force_authenticate(user=self.user1)

        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id - 1,
                    'user_pk': self.user1.id
                }
            )
        )

        self.assertFalse(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_grade_detail_with_invalid_user(self):
        self.client.force_authenticate(user=self.user1)

        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id - 1
                }
            )
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_grade_posting_with_anonymous_user(self):
        request = self.client.post(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            ),
            data={'value': 3.12},
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_grade_posting_with_student(self):
        self.client.force_authenticate(user=self.user1)

        request = self.client.post(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            ),
            data={'value': 3.12},
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'You do not have permission to perform this action.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_grade_posting_with_teacher(self):
        self.client.force_authenticate(user=self.user3)

        request = self.client.post(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            ),
            data={'value': 3.12},
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_grade_posting_with_invalid_subject_id(self):
        self.client.force_authenticate(user=self.user3)

        request = self.client.post(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id - 1,
                    'user_pk': self.user1.id
                }
            ),
            data={'value': 3.12},
            format='json'
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_grade_posting_with_different_subject(self):
        self.client.force_authenticate(user=self.user3)

        request = self.client.post(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject2.id,
                    'user_pk': self.user1.id
                }
            ),
            data={'value': 3.12},
            format='json'
        )

        self.assertEqual(
            request.data['detail'],
            'You do not have permission to perform this action.'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_grade_posting_with_invalid_user_id(self):
        self.client.force_authenticate(user=self.user3)

        request = self.client.post(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id - 1
                }
            ),
            data={'value': 3.12},
            format='json'
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_grade_posting_with_too_low_grade(self):
        self.client.force_authenticate(user=self.user3)

        request = self.client.post(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            ),
            data={'value': 1.23},
            format='json'
        )

        self.assertEqual(
            request.data['value'],
            ['Ensure this value is greater than or equal to 2.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_grade_posting_with_too_high_grade(self):
        self.client.force_authenticate(user=self.user3)

        request = self.client.post(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            ),
            data={'value': 6.81},
            format='json'
        )

        self.assertEqual(
            request.data['value'],
            ['Ensure this value is less than or equal to 6.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

class StudentsListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:students-list'

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='Maths')

        self.user = User.objects.create(
            username='tester',
            first_name='test',
            last_name='user',
            email='tester@gmail.com',
            password='pass'
        )

        self.student = Student.objects.create(
            user=self.user,
            clazz=self.clazz,
            info='I am the lord of the rings.'
        )

    def test_students_list_with_anonymous_user(self):
        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            )
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_students_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            )
        )

        self.assertTrue(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_students_list_with_invalid_clazz_letter(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': 'Z'
                }
            )
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)


class ClassesListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:classes-number-list'

        self.clazz = Class.objects.create(number=10, letter='A')

        self.user = User.objects.create(
            username='tester',
            first_name='test',
            last_name='user',
            email='tester@gmail.com',
            password='pass'
        )

        self.student = Student.objects.create(
            user=self.user,
            clazz=self.clazz,
            info='I am the lord of the rings.'
        )

    def test_classes_list_with_anonymous_user(self):
        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'class_number': self.clazz.number
                }
            )
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_classes_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'class_number': self.clazz.number
                }
            )
        )
        
        self.assertTrue(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
