from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from students.models import Class, Subject, Student, Teacher

from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer


class NewsStudentsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'news:students_news-list'
        self.detail_view_name = 'news:students_news-detail'

        self.user = User(username='test', email='test@test.com')
        self.user.set_password('password123')
        self.user.save()

        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)
        self.news = News.objects.create(
            title='test news',
            content='test news content',
            class_number=self.clazz.number,
            class_letter=self.clazz.letter,
            author=self.user,
        )
        self.comment = Comment.objects.create(
            news=self.news,
            author=self.user,
            content='test comment content'
        )

    def test_news_list_with_anonymous_user(self):
        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_news_detail_with_anonymous_user(self):
        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.news.id}))

        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_news_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.list_view_name))

        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.news.id}))

        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_list_with_teacher_account(self):
        teacher_user = User.objects.create(username='teacher', password='123456')

        subject = Subject.objects.create(title='Maths')
        teacher = Teacher.objects.create(user=teacher_user, subject=subject)

        self.client.force_authenticate(user=teacher_user)

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(
            response.data['detail'], 'Only students are allowed to view and modify this content.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_news_list_with_same_class(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.list_view_name))

        results = response.data['results']
        self.assertEqual(results[0]['title'], self.news.title)
        self.assertEqual(results[0]['content'], self.news.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_list_with_different_class(self):
        self.client.force_authenticate(user=self.user)
        self.student.clazz = Class.objects.create(number=11, letter='V')

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(response.data['results'], [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_creation_with_empty_title(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = ''
        post_data = NewsSerializer(self.news).data

        response = self.client.post(reverse(self.list_view_name), post_data, format='json')

        self.assertEqual(response.data['title'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_short_title(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = 'ab'
        post_data = NewsSerializer(self.news).data

        response = self.client.post(reverse(self.list_view_name), post_data, format='json')

        self.assertEqual(response.data['title'], ['Ensure this field has at least 3 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_long_title(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = 'new title' * 120
        post_data = NewsSerializer(self.news).data

        response = self.client.post(reverse(self.list_view_name), post_data, format='json')

        self.assertEqual(
            response.data['title'], ['Ensure this field has no more than 100 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_empty_content(self):
        self.client.force_authenticate(user=self.user)
        self.news.content = ''
        post_data = NewsSerializer(self.news).data

        response = self.client.post(reverse(self.list_view_name), post_data, format='json')

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_short_content(self):
        self.client.force_authenticate(user=self.user)
        self.news.content = 'abc'
        post_data = NewsSerializer(self.news).data

        response = self.client.post(reverse(self.list_view_name), post_data, format='json')

        self.assertEqual(response.data['content'], ['Ensure this field has at least 5 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_long_content(self):
        self.client.force_authenticate(user=self.user)
        self.news.content = 'content' * 10000
        post_data = NewsSerializer(self.news).data

        response = self.client.post(reverse(self.list_view_name), post_data, format='json')

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 10000 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_valid_data(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = 'new title'
        self.news.content = 'content'
        post_data = NewsSerializer(self.news).data

        response = self.client.post(reverse(self.list_view_name), post_data, format='json')

        self.assertEqual(response.data['title'], self.news.title)
        self.assertEqual(response.data['content'], self.news.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_news_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.news.id + 1}))

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_news_detail_with_valid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.news.id}))

        self.assertEqual(response.data['id'], self.news.id)
        self.assertEqual(response.data['title'], self.news.title)
        self.assertEqual(response.data['content'], self.news.content)

        comments_data = response.data['comments']
        self.assertEqual(comments_data[0]['content'], self.comment.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_update_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        new_user = User.objects.create(username='test2', password='pass')
        new_student = Student.objects.create(user=new_user, clazz=self.clazz)
        self.news.author = new_user
        self.news.save()

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            {'title': 'test'},
            format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_news_update_with_empty_title(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            {'title': ''},
            format='json'
        )

        self.assertEqual(response.data['title'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_too_short_title(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            {'title': 'ab'},
            format='json'
        )

        self.assertEqual(response.data['title'], ['Ensure this field has at least 3 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_too_long_title(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            {'title': 'title' * 500},
            format='json'
        )

        self.assertEqual(
            response.data['title'], ['Ensure this field has no more than 100 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_empty_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            {'content': ''},
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_too_short_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            {'content': 'abc'},
            format='json'
        )

        self.assertEqual(response.data['content'], ['Ensure this field has at least 5 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_too_long_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            {'content': 'abc' * 10000},
            format='json'
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 10000 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_valid_data(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id}),
            {'title': 'new test title', 'content': 'new test content'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        new_user = User.objects.create(username='test2', password='pass')
        new_student = Student.objects.create(user=new_user, clazz=self.clazz)
        self.news.author = new_user
        self.news.save()

        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.news.id}))

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_news_deletion_with_invalid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.news.id + 1})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_news_deletion_with_valid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.news.id}))

        self.assertEqual(News.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class NewsTeachersViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'news:teachers_news-list'
        self.detail_view_name = 'news:teachers_news-detail'

        self.user = User(username='test', email='sisko@gmail.com')
        self.user.set_password('password123')
        self.user.save()

        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='Maths')
        self.student = Teacher.objects.create(user=self.user, subject=self.subject)
        self.news = News.objects.create(
            title='test news title',
            content='test news content',
            class_number=self.clazz.number,
            class_letter=self.clazz.letter,
            author=self.user,
        )
        self.comment = Comment.objects.create(
            news=self.news,
            author=self.user,
            content='test comment content'
        )

    def test_news_list_with_anonymous_user(self):
        response = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            )
        )

        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_news_detail_with_anonymous_user(self):
        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            )
        )

        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_news_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            )
        )

        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            )
        )

        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_list_with_student_account(self):
        student_user = User.objects.create(username='teacher', password='123456')
        student = Student.objects.create(user=student_user, clazz=self.clazz)

        self.client.force_authenticate(user=student_user)

        response = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                }
            )
        )

        self.assertEqual(
            response.data['detail'], 'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_news_list_with_same_class(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            )
        )

        results = response.data['results']
        self.assertEqual(results[0]['title'], self.news.title)
        self.assertEqual(results[0]['content'], self.news.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_list_with_different_class(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': 9,
                    'class_letter': 'V'
                }
            )
        )

        self.assertEqual(response.data['results'], [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_creation_with_empty_title(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = ''
        post_data = NewsSerializer(self.news).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['title'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_short_title(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = 'ab'
        post_data = NewsSerializer(self.news).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['title'], ['Ensure this field has at least 3 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_long_title(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = 'new title' * 120
        post_data = NewsSerializer(self.news).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['title'], ['Ensure this field has no more than 100 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_empty_content(self):
        self.client.force_authenticate(user=self.user)
        self.news.content = ''
        post_data = NewsSerializer(self.news).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_short_content(self):
        self.client.force_authenticate(user=self.user)
        self.news.content = 'abc'
        post_data = NewsSerializer(self.news).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], ['Ensure this field has at least 5 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_long_content(self):
        self.client.force_authenticate(user=self.user)
        self.news.content = 'content' * 10000
        post_data = NewsSerializer(self.news).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 10000 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_valid_data(self):
        self.client.force_authenticate(user=self.user)
        self.news.title = 'new title'
        self.news.content = 'content'
        post_data = NewsSerializer(self.news).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['title'], self.news.title)
        self.assertEqual(response.data['content'], self.news.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_news_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id + 1
                }
            )
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_news_detail_with_valid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            )
        )

        self.assertEqual(response.data['id'], self.news.id)
        self.assertEqual(response.data['title'], self.news.title)
        self.assertEqual(response.data['content'], self.news.content)

        comments_data = response.data['comments']
        self.assertEqual(comments_data[0]['content'], self.comment.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_update_with_empty_title(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            ),
            {'title': ''},
            format='json'
        )

        self.assertEqual(response.data['title'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_too_short_title(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            ),
            {'title': 'ab'},
            format='json'
        )

        self.assertEqual(response.data['title'], ['Ensure this field has at least 3 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_too_long_title(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            ),
            {'title': 'new title' * 100},
            format='json'
        )

        self.assertEqual(
            response.data['title'], ['Ensure this field has no more than 100 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_empty_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            ),
            {'content': ''},
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_too_short_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            ),
            {'content': 'ab'},
            format='json'
        )

        self.assertEqual(response.data['content'], ['Ensure this field has at least 5 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_too_long_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            ),
            {'content': 'new title' * 5000},
            format='json'
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 10000 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_update_with_valid_data(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            ),
            {'title': 'new title', 'content': 'new content'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_deletion_with_invalid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id + 2
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_news_deletion_with_valid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'pk': self.news.id
                }
            )
        )

        self.assertEqual(News.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class NewsTeachersClassNumberListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.view_name = 'news:teachers_class_number_list'

        self.user1 = User(username='test', email='sisko@gmail.com')
        self.user1.set_password('password123')
        self.user1.save()

        self.user2 = User(username='arigato', email='wen@gmail.com')
        self.user2.set_password('qwerty')
        self.user2.save()

        self.user3 = User(username='teacher', email='teach@gmail.com')
        self.user3.set_password('qwerty')
        self.user3.save()

        self.subject = Subject.objects.create(title='Maths')
        self.teacher = Teacher.objects.create(user=self.user3, subject=self.subject)

        self.clazz_number = 10
        self.clazz1 = Class.objects.create(number=self.clazz_number, letter='A')
        self.clazz2 = Class.objects.create(number=self.clazz_number, letter='B')
        self.clazz3 = Class.objects.create(number=self.clazz_number + 1, letter='V')

        self.student1 = Student.objects.create(user=self.user1, clazz=self.clazz1)
        self.student2 = Student.objects.create(user=self.user2, clazz=self.clazz2)

        self.news1 = News.objects.create(
            title='test news title 1',
            content='test news content 1',
            class_number=self.clazz1.number,
            class_letter=self.clazz1.letter,
            author=self.user1,
        )
        self.news2 = News.objects.create(
            title='test news title 2',
            content='test news content 2',
            class_number=self.clazz2.number,
            class_letter=self.clazz2.letter,
            author=self.user2,
        )

    def test_news_list_with_anonymous_user(self):
        response = self.client.get(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number})
        )

        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_news_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user3)

        response = self.client.get(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number})
        )

        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_list_with_student_account(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number})
        )

        self.assertEqual(
            response.data['detail'], 'Only teachers are allowed to view and modify this content.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_news_creation_with_empty_title(self):
        self.client.force_authenticate(user=self.user3)
        self.news1.title = ''
        post_data = NewsSerializer(self.news1).data

        response = self.client.post(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number}),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['title'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_short_title(self):
        self.client.force_authenticate(user=self.user3)
        self.news1.title = 'ab'
        post_data = NewsSerializer(self.news1).data

        response = self.client.post(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number}),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['title'], ['Ensure this field has at least 3 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_long_title(self):
        self.client.force_authenticate(user=self.user3)
        self.news1.title = 'test' * 50
        post_data = NewsSerializer(self.news1).data

        response = self.client.post(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number}),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['title'], ['Ensure this field has no more than 100 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_empty_content(self):
        self.client.force_authenticate(user=self.user3)
        self.news1.content = ''
        post_data = NewsSerializer(self.news1).data

        response = self.client.post(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number}),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_short_content(self):
        self.client.force_authenticate(user=self.user3)
        self.news1.content = 'abc'
        post_data = NewsSerializer(self.news1).data

        response = self.client.post(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number}),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], ['Ensure this field has at least 5 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_too_long_content(self):
        self.client.force_authenticate(user=self.user3)
        self.news1.content = 'abc' * 10000
        post_data = NewsSerializer(self.news1).data

        response = self.client.post(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number}),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 10000 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_creation_with_valid_data(self):
        self.client.force_authenticate(user=self.user3)
        self.news1.title = 'new title'
        self.news1.content = 'new content'
        post_data = NewsSerializer(self.news1).data

        response = self.client.post(
            reverse(self.view_name, kwargs={'class_number': self.clazz_number}),
            post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class NewsStudentsCommentsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'news:students_news_comments-list'
        self.detail_view_name = 'news:students_news_comments-detail'

        self.user = User.objects.create(username='test1', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.student = Student.objects.create(user=self.user, clazz=self.clazz)
        self.news = News.objects.create(
            title='test news title',
            content='test news content',
            class_number=self.clazz.number,
            class_letter=self.clazz.letter,
            author=self.user,
        )
        self.comment = Comment.objects.create(
            news=self.news,
            author=self.user,
            content='test comment content'
        )

    def test_comment_creation_with_empty_content(self):
        self.client.force_authenticate(user=self.user)
        self.comment.content = ''
        post_data = CommentSerializer(self.comment).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'students_news_pk': self.news.id}),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_creation_with_too_long_content(self):
        self.client.force_authenticate(user=self.user)
        self.comment.content = 'content' * 1024
        post_data = CommentSerializer(self.comment).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'students_news_pk': self.news.id}),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 2048 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_creation_with_valid_content(self):
        self.client.force_authenticate(user=self.user)
        self.comment.content = 'new content'
        post_data = CommentSerializer(self.comment).data

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'students_news_pk': self.news.id}),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], self.comment.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_update_with_empty_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'students_news_pk': self.news.id, 'pk': self.comment.id}
            ),
            {'content': ''},
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        new_user = User.objects.create(username='test2', password='pass')
        new_student = Student.objects.create(user=new_user, clazz=self.clazz)
        self.comment.author = new_user
        self.comment.save()

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'students_news_pk': self.news.id, 'pk': self.comment.id}
            ),
            {'content': 'new test comment content'},
            format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_update_with_too_long_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'students_news_pk': self.news.id, 'pk': self.comment.id}
            ),
            {'content': 'title' * 1024},
            format='json'
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 2048 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update_with_valid_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={'students_news_pk': self.news.id, 'pk': self.comment.id}
            ),
            {'content': 'updated content'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_deletion_with_invalid_news_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'students_news_pk': self.news.id + 1, 'pk': self.comment.id}
            )
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_deletion_with_invalid_comment_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'students_news_pk': self.news.id, 'pk': self.comment.id + 1}
            )
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        new_user = User.objects.create(username='test3', password='pass')
        new_student = Student.objects.create(user=new_user, clazz=self.clazz)
        self.comment.author = new_user
        self.comment.save()

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'students_news_pk': self.news.id, 'pk': self.comment.id}
            )
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_deletion_with_valid_ids(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={'students_news_pk': self.news.id, 'pk': self.comment.id}
            )
        )

        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class NewsTeachersCommentsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'news:teachers_news_comments-list'
        self.detail_view_name = 'news:teachers_news_comments-detail'

        self.user = User.objects.create(username='test1', password='pass')
        self.clazz = Class.objects.create(number=10, letter='A')
        self.subject = Subject.objects.create(title='Literature')
        self.teacher = Teacher.objects.create(user=self.user, subject=self.subject)

        self.news = News.objects.create(
            title='test news title',
            content='test news content',
            class_number=self.clazz.number,
            class_letter=self.clazz.letter,
            author=self.user,
        )
        self.comment = Comment.objects.create(
            news=self.news,
            author=self.user,
            content='test comment content'
        )

    def test_comment_creation_with_empty_content(self):
        self.client.force_authenticate(user=self.user)
        self.comment.content = ''
        post_data = CommentSerializer(self.comment).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_creation_with_too_long_content(self):
        self.client.force_authenticate(user=self.user)
        self.comment.content = 'content' * 1024
        post_data = CommentSerializer(self.comment).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 2048 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_creation_with_valid_content(self):
        self.client.force_authenticate(user=self.user)
        self.comment.content = 'This is a very nice platorm, man!'
        post_data = CommentSerializer(self.comment).data

        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id
                }
            ),
            post_data,
            format='json'
        )

        self.assertEqual(response.data['content'], self.comment.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_update_with_empty_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id,
                    'pk': self.comment.id
                }
            ),
            {'content': ''},
            format='json'
        )

        self.assertEqual(response.data['content'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        new_user = User.objects.create(username='test2', password='pass')
        Teacher.objects.create(user=new_user, subject=self.subject)
        self.comment.author = new_user
        self.comment.save()

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id,
                    'pk': self.comment.id
                }
            ),
            {'content': 'new test content'},
            format='json'
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_update_with_too_long_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id,
                    'pk': self.comment.id
                }
            ),
            {'content': 'new test content' * 1024},
            format='json'
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 2048 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update_with_valid_content(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id,
                    'pk': self.comment.id
                }
            ),
            {'content': 'new test content'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_deletion_with_invalid_news_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id + 1,
                    'pk': self.comment.id
                }
            )
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_deletion_with_invalid_comment_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id,
                    'pk': self.comment.id + 5
                }
            )
        )

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        new_user = User.objects.create(username='test3', password='pass')
        Teacher.objects.create(user=new_user, subject=self.subject)
        self.comment.author = new_user
        self.comment.save()

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id,
                    'pk': self.comment.id
                }
            )
        )

        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_deletion_with_valid_ids(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'class_number': self.clazz.number,
                    'class_letter': self.clazz.letter,
                    'teachers_news_pk': self.news.id,
                    'pk': self.comment.id
                }
            )
        )

        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
