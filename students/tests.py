from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from datetime import datetime, timedelta

from .models import Class, Student, Subject, Exam, News, Homework, Comment
from .serializers import NewsSerializer, CommentSerializer


class RegisterViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:register'

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

        self.assertEqual(
            user_data['username'],
            user_data['first_name'] + '_' + user_data['last_name']
        )
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


class ProfileViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:profile'

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
        request = self.client.get(reverse(self.view_name))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_profile_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(reverse(self.view_name))

        self.assertEqual(
            self.student.user.username, request.data['user']['username']
        )
        self.assertEqual(
            self.student.clazz.number, request.data['clazz']['number']
        )
        self.assertEqual(
            self.student.clazz.letter, request.data['clazz']['letter']
        )
        self.assertNotIn('password', request.data['user'])
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class ExamsViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:exams'

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
        request = self.client.get(reverse(self.view_name))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_exams_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(reverse(self.view_name))

        self.assertIn(self.subject.title, request.data[0]['subject']['title'])
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_exams_with_expired_date(self):
        self.client.force_authenticate(user=self.user)
        self.exam.date -= timedelta(days=5)
        self.exam.save()

        request = self.client.get(reverse(self.view_name))

        self.assertEqual(request.data, [])
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class NewsListViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:news-list'

        self.user = User(username='test', email='sisko@gmail.com')
        self.user.set_password('password123')
        self.user.save()

        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)
        self.news = News.objects.create(
            title='test_news',
            content='blablabla',
            author=self.student,
        )


    def test_news_list_with_anonymous_user(self):
        request = self.client.get(reverse(self.view_name))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_news_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(reverse(self.view_name))

        self.assertIsNotNone(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_news_list_with_same_class(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(reverse(self.view_name))

        self.assertEqual(request.data[0]['title'], self.news.title)
        self.assertEqual(request.data[0]['content'], self.news.content)
        self.assertEqual(
            request.data[0]['author']['user'], self.user.username
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_news_list_with_different_class(self):
        self.client.force_authenticate(user=self.user)
        self.student.clazz = Class.objects.create(number=11, letter='V')

        request = self.client.get(reverse(self.view_name))

        self.assertEqual(request.data, [])
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_news_list_addition_with_empty_title(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = ''
        post_data = NewsSerializer(self.news).data

        request = self.client.post(
            reverse(self.view_name), post_data, format='json'
        )

        self.assertEqual(
            request.data['title'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


    def test_news_list_addition_with_empty_content(self):
        self.client.force_authenticate(user=self.user)
        self.news.content = ''
        post_data = NewsSerializer(self.news).data

        request = self.client.post(
            reverse(self.view_name), post_data, format='json'
        )

        self.assertEqual(
            request.data['content'], ['This field may not be blank.']
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


    def test_news_list_addition_with_valid_data(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = 'testNews'
        self.news.content = 'testContent'
        post_data = NewsSerializer(self.news).data

        request = self.client.post(
            reverse(self.view_name), post_data, format='json'
        )

        self.assertEqual(request.data['content'], self.news.content)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


class NewsDetailViewTestCase(APITestCase):
    
    # TODO: Implement more tests

    def setUp(self):
        self.client = APIClient()
        self.detail_view_name = 'students:news-detail'

        self.user = User.objects.create(username='test1', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)
        self.news = News.objects.create(
            title='test_news',
            content='blablabla',
            author=self.student,
        )
        self.comment = Comment.objects.create(
            news=self.news,
            posted_by=self.student,
            content='This is a very nice platform!'
        )


    def test_news_detail_with_anonymous_user(self):
        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id})
        )

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_news_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id})
        )

        self.assertIsNotNone(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_news_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id + 1})
        )

        self.assertEqual(request.data['detail'], 'Not found.')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)


    def test_news_detail_with_valid_id(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id})
        )

        self.assertEqual(request.data['id'], self.news.id)
        self.assertEqual(request.data['title'], self.news.title)
        self.assertEqual(request.data['content'], self.news.content)
        self.assertEqual(request.data['author']['user'], self.user.username)

        comments_data = request.data['comment_set']
        self.assertEqual(comments_data[0]['content'], self.comment.content)
        self.assertEqual(
            comments_data[0]['posted_by']['user'], self.user.username
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_news_update(self):
        self.client.force_authenticate(user=self.user)

        put_data = {
            'title': 'Amazing!',
            'content': 'This should work perfectly!'
        }

        request = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            put_data,
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)


class CommentsViewSetTestCase(APITestCase):

    # TODO: Implement more tests

    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'students:comments-list'
        self.detail_view_name = 'students:comments-detail'

        self.user = User.objects.create(username='test1', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)
        self.news = News.objects.create(
            title='test_news',
            content='blablabla',
            author=self.student,
        )
        self.comment = Comment.objects.create(
            news=self.news,
            posted_by=self.student,
            content='This is a very nice platform!'
        )


    def test_comment_addition(self):
        self.client.force_authenticate(user=self.user)
        self.comment.content = 'This is a very nice platorm, man!'
        post_data = CommentSerializer(self.comment).data

        request = self.client.post(
            reverse(self.list_view_name, kwargs={'news_pk': self.news.id}),
            post_data,
            format='json'
        )

        self.assertEqual(request.data['content'], self.comment.content)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


    def test_comment_update(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'news_pk': self.news.id, 'pk': self.comment.id}
            ),
            {'content': '+1!'},
            format='json'
        )

        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_comment_deletion(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'news_pk': self.news.id, 'pk': self.comment.id}
            )
        )

        self.assertEqual(
            request.data['message'], 'Comment successfully deleted.'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class HomeworksViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.view_name = 'students:homeworks'

        self.subject = Subject.objects.create(title='test_subject')
        self.user = User.objects.create(username='test', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)
        self.homework = Homework.objects.create(
            subject=self.subject,
            clazz=self.clazz,
            deadline=datetime.now().date(),
            details='something interesting'
        )


    def test_homeworks_with_anonymous_user(self):
        request = self.client.get(reverse(self.view_name))

        self.assertEqual(
            request.data['detail'],
            'Authentication credentials were not provided.'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_homeworks_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        request = self.client.get(reverse(self.view_name))

        self.assertIsNotNone(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_homeworks_with_expired_date(self):
        self.client.force_authenticate(user=self.user)
        self.homework.deadline -= timedelta(days=5)
        self.homework.save()

        request = self.client.get(reverse(self.view_name))

        self.assertEqual(request.data, [])
        self.assertEqual(request.status_code, status.HTTP_200_OK)
