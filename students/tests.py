from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from students.models import Class, Subject, Student, Teacher
from students.serializers import StudentProfileSerializer


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
            request.data['message'],
            'You can only update your own profile.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


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
        self.student1.profile_image_url = 'https://scontent-fra3-1.xx.fbcdn.net/v/l/t1.0-9/14237770_10207844537094902_7208336482223852857_n.jpg?oh=a7ead37183048f79ca1f66e6b7121569&oe=59220B3C'
        put_data = StudentProfileSerializer(self.student1).data

        request = self.client.put(
            reverse(self.view_name, kwargs={'pk': self.user1.id}),
            put_data,
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)
