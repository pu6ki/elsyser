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
                'email': 'test@test.test',
                'password': 'testerpassword123456',
            },
            'clazz': {
                'number': 10,
                'letter': 'A',
            }
        }

    def test_registration_with_empty_email(self):
        self.test_data['user']['email'] = ''

        response = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            response.data['user']['email'], ['This field may not be blank.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_email(self):
        self.test_data['user']['email'] = 'tester'

        response = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            response.data['user']['email'], ['Enter a valid email address.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_empty_password(self):
        self.test_data['user']['password'] = ''

        response = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            response.data['user']['password'], ['This field may not be blank.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_too_short_password(self):
        self.test_data['user']['password'] = 'test'

        response = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            response.data['user']['password'],
            ['Ensure this field has at least 8 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_too_long_password(self):
        self.test_data['user']['password'] = 'test123' * 123

        response = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            response.data['user']['password'],
            ['Ensure this field has no more than 64 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_clazz(self):
        self.test_data['clazz']['number'] = 0

        response = self.client.post(
            reverse(self.view_name), self.test_data, format='json'
        )

        self.assertEqual(
            response.data['clazz']['number'], ['"0" is not a valid choice.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_valid_data(self):
        response = self.client.post(reverse(self.view_name), self.test_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['message'],
            'Verification email has been sent to {}.'.format(self.test_data['user']['email'])
        )


class AccountActivationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_view = reverse('students:register')
        self.login_view = reverse('students:login')
        self.view_name = 'students:activation'

        self.registration_data = {
            'user': {
                'username': 'tester123',
                'first_name': 'test',
                'last_name': 'testoff',
                'email': 'test@test.test',
                'password': 'testerpassword123456',
            },
            'clazz': {
                'number': 10,
                'letter': 'A',
            }
        }

        self.login_data = {
            'email_or_username': self.registration_data['user']['username'],
            'password': self.registration_data['user']['password']
        }

    def test_registration_and_login_with_unactivated_account(self):
        register_response = self.client.post(
            self.registration_view,
            data=self.registration_data,
            format='json'
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            register_response.data['message'],
            'Verification email has been sent to {}.'.format(self.registration_data['user']['email'])
        )

        login_response = self.client.post(self.login_view, data=self.login_data, format='json')

        self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            login_response.data['non_field_errors'],
            ['Unable to log in with provided credentials.']
        )

    def test_activation_with_invalid_activation_key(self):
        register_response = self.client.post(
            self.registration_view,
            data=self.registration_data,
            format='json'
        )
        created_student = Student.objects.get(
            user__username=self.registration_data['user']['username']
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            register_response.data['message'],
            'Verification email has been sent to {}.'.format(created_student.user.email)
        )

        activation_response = self.client.put(
            reverse(
                self.view_name,
                kwargs={
                    'activation_key': created_student.activation_key + 'f'
                }
            )
        )

        self.assertEqual(activation_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_activation_and_login_with_valid_activation_key(self):
        register_response = self.client.post(
            self.registration_view,
            data=self.registration_data,
            format='json'
        )
        created_student = Student.objects.get(
            user__username=self.registration_data['user']['username']
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            register_response.data['message'],
            'Verification email has been sent to {}.'.format(created_student.user.email)
        )

        activation_response = self.client.put(
            reverse(
                self.view_name,
                kwargs={
                    'activation_key': created_student.activation_key
                }
            )
        )

        self.assertEqual(activation_response.status_code, status.HTTP_204_NO_CONTENT)
        
        login_response = self.client.post(self.login_view, data=self.login_data, format='json')
        
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(login_response.data['id'], created_student.id)


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
        response = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(
            response.data['email_or_username'], ['This field may not be blank.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_blank_password(self):
        self.post_data['email_or_username'] = self.user.email
        self.post_data['password'] = ''

        response = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(
            response.data['password'], ['This field may not be blank.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_email_or_username(self):
        self.post_data['email_or_username'] = 'invalid'

        response = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(
            response.data['non_field_errors'],
            ['Unable to log in with provided credentials.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_password(self):
        self.post_data['email_or_username'] = self.user.email
        self.post_data['password'] = 'invalidpassword'

        response = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(
            response.data['non_field_errors'],
            ['Unable to log in with provided credentials.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_valid_email_and_password(self):
        self.post_data['email_or_username'] = self.user.email

        response = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(self.token.key, response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_valid_username_and_password(self):
        self.post_data['email_or_username'] = self.user.username

        response = self.client.post(reverse(self.view_name), self.post_data)

        self.assertEqual(self.token.key, response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChangePasswordViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view = reverse('students:change-password')

        self.user_password = 'mys3cr3tp@ssw0rd'
        self.new_password = 'b3stk3pts3cr3t'
        self.user = User.objects.create_user(username='tester', password=self.user_password)

        self.put_data = {
            'old_password': self.user_password,
            'new_password': self.new_password
        }

    def test_password_change_with_non_authenticated_user(self):
        response = self.client.put(self.view, data=self.put_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_change_with_non_matching_old_password(self):
        self.client.force_authenticate(user=self.user)

        self.put_data['old_password'] += 'bla'
        response = self.client.put(self.view, data=self.put_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Wrong password.')

    def test_password_change_with_too_short_new_password(self):
        self.client.force_authenticate(user=self.user)

        self.put_data['new_password'] = 'bla'
        response = self.client.put(self.view, data=self.put_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['new_password'],
            ['This password is too short. It must contain at least 8 characters.']
        )

    def test_password_change_with_too_long_new_password(self):
        self.client.force_authenticate(user=self.user)

        self.put_data['new_password'] = self.new_password * 1000
        response = self.client.put(self.view, data=self.put_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['new_password'],
            ['Ensure this field has no more than 64 characters.']
        )

    def test_password_change_with_matching_passwords(self):
        self.client.force_authenticate(user=self.user)

        self.put_data['new_password'] = self.new_password
        response = self.client.put(self.view, data=self.put_data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.user.check_password(self.new_password))


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
        response = self.client.get(
            reverse(self.view_name, kwargs={'pk': self.user1.id})
        )

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_with_own_user(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(self.view_name, kwargs={'pk': self.user1.id})
        )

        self.assertEqual(
            self.student1.user.username, response.data['user']['username']
        )
        self.assertEqual(
            self.student1.clazz.number, response.data['clazz']['number']
        )
        self.assertEqual(
            self.student1.clazz.letter, response.data['clazz']['letter']
        )
        self.assertEqual(self.student1.info, response.data['info'])
        self.assertTrue(response.data['can_edit'])
        self.assertNotIn('password', response.data['user'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_with_other_user(self):
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(
            reverse(self.view_name, kwargs={'pk': self.user1.id})
        )

        self.assertEqual(
            self.student1.user.username, response.data['user']['username']
        )
        self.assertEqual(
            self.student1.clazz.number, response.data['clazz']['number']
        )
        self.assertEqual(
            self.student1.clazz.letter, response.data['clazz']['letter']
        )
        self.assertEqual(self.student1.info, response.data['info'])
        self.assertFalse(response.data['can_edit'])
        self.assertNotIn('password', response.data['user'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update_of_another_user(self):
        self.client.force_authenticate(user=self.user2)
        self.student1.user.username = 'MyNewUsername'
        self.student1.user.first_name = 'John'
        self.student1.user.last_name = 'Travolta'
        put_data = StudentProfileSerializer(self.student1).data

        response = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_update_with_invalid_username(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.user.username = ''
        put_data = StudentProfileSerializer(self.student1).data

        response = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['user']['username'], ['This field may not be blank.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_invalid_first_name(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.user.first_name = ''
        put_data = StudentProfileSerializer(self.student1).data

        response = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['user']['first_name'], ['This field may not be blank.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_invalid_last_name(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.user.last_name = ''
        put_data = StudentProfileSerializer(self.student1).data

        response = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['user']['last_name'], ['This field may not be blank.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_invalid_profile_picture_url(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.profile_image_url = 'https://www.youtube.com/watch?v=vSoUp-SxLrQ'
        put_data = StudentProfileSerializer(self.student1).data

        response = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(
            response.data['profile_image_url'], ['URL is not a picture.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_valid_data(self):
        self.client.force_authenticate(user=self.user1)
        self.student1.user.username = 'MyNewUsername'
        self.student1.user.first_name = 'John'
        self.student1.user.last_name = 'Travolta'
        self.student1.profile_image_url = 'http://books.sulla.bg/wp-content/uploads/2011/11/kurt_vonnegut.jpg'
        put_data = StudentProfileSerializer(self.student1).data

        response = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentsListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:students-list'
        self.url = reverse(self.view_name)

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

    def test_students_list_with_anonymous_user(self):
        response = self.client.get(
            self.url,
            {
                'class_number': self.clazz.number,
                'class_letter': self.clazz.letter
            }
        )

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_students_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.url,
            {
                'class_number': self.clazz.number,
                'class_letter': self.clazz.letter
            }
        )

        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_students_list_with_invalid_class_number(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.url,
            {
                'class_number': 42,
                'class_letter': self.clazz.letter
            }
        )

        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)        

    def test_students_list_with_invalid_class_letter(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.url,
            {
                'class_number': self.clazz.number,
                'class_letter': 'z'
            }
        )

        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ClassesListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:classes-list'
        self.url = reverse(self.view_name)

        self.class_number = 10
        self.clazz1 = Class.objects.create(number=self.class_number, letter='A')
        self.clazz2 = Class.objects.create(number=self.class_number + 1, letter='V')

        self.user = User.objects.create(
            username='tester',
            first_name='test',
            last_name='user',
            email='tester@gmail.com',
            password='pass'
        )
        self.student = Student.objects.create(
            user=self.user,
            clazz=self.clazz1,
            info='I am the lord of the rings.'
        )

    def test_classes_list_with_anonymous_user(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_classes_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_classes_list_with_class_number_param(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url, {'number': self.class_number})

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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

    def test_subject_list_with_anonymous_user(self):
        response = self.client.get(
            reverse(self.view_name, kwargs={'subject_pk': self.subject.id})
        )

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subject_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse(self.view_name, kwargs={'subject_pk': self.subject.id})
        )

        self.assertEqual(response.data[0]['value'], self.grade2.value)
        self.assertEqual(response.data[1]['value'], self.grade1.value)
        self.assertEqual(
            response.data[0]['student']['user']['username'],
            self.user.username
        )
        self.assertEqual(
            response.data[1]['student']['user']['username'],
            self.user.username
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subject_list_with_invalid_subject_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(self.view_name, kwargs={'subject_pk': self.subject.id - 1})
        )

        self.assertFalse(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
        response = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            )
        )

        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_grade_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            )
        )

        self.assertEqual(response.data[0]['value'], self.grade1.value)
        self.assertEqual(
            response.data[0]['student']['user']['username'],
            self.user1.username
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_grade_detail_of_another_user(self):
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id
                }
            )
        )

        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_grade_detail_with_non_graded_subject(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id - 1,
                    'user_pk': self.user1.id
                }
            )
        )

        self.assertFalse(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_grade_detail_with_invalid_user(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(
                self.view_name,
                kwargs={
                    'subject_pk': self.subject1.id,
                    'user_pk': self.user1.id - 1
                }
            )
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_grade_posting_with_anonymous_user(self):
        response = self.client.post(
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
            response.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_grade_posting_with_student(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
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
            response.data['detail'],
            'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_grade_posting_with_teacher(self):
        self.client.force_authenticate(user=self.user3)

        response = self.client.post(
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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_grade_posting_with_invalid_subject_id(self):
        self.client.force_authenticate(user=self.user3)

        response = self.client.post(
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

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_grade_posting_with_different_subject(self):
        self.client.force_authenticate(user=self.user3)

        response = self.client.post(
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
            response.data['detail'],
           'You can modify content linked only with your subject.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_grade_posting_with_invalid_user_id(self):
        self.client.force_authenticate(user=self.user3)

        response = self.client.post(
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

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_grade_posting_with_too_low_grade(self):
        self.client.force_authenticate(user=self.user3)

        response = self.client.post(
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
            response.data['value'],
            ['Ensure this value is greater than or equal to 2.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_grade_posting_with_too_high_grade(self):
        self.client.force_authenticate(user=self.user3)

        response = self.client.post(
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
            response.data['value'],
            ['Ensure this value is less than or equal to 6.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
