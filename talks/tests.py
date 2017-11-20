from datetime import datetime, timedelta

from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from .serializers import MeetupSerializer, TalkSerializer
from .models import Meetup, Talk

# TODO: Implement tests

class MeetupsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'talks:meetups-list'
        self.detail_view_name = 'talks:meetups-detail'
        self.serializer_class = MeetupSerializer

        self.normal_user = User.objects.create(username='test', password='pass')
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@admin.com', password='s3cr3t'
        )

        now = datetime.now().date()
        self.upcoming_meetup = Meetup.objects.create(date=now + timedelta(days=3))
        self.past_meetup = Meetup.objects.create(date=now - timedelta(days=3))

    def test_meetups_list_with_anonymous_user(self):
        pass

    def test_meetups_list_with_authenticated_user(self):
        pass

    def test_meetups_list_past_filtering(self):
        pass

    def test_meetups_list_upcoming_filtering(self):
        pass

    def test_meetups_detail_with_anonymous_user(self):
        pass

    def test_meetups_detail_with_authenticated_user(self):
        pass

    def test_meetups_create_with_normal_user(self):
        pass

    def test_meetups_create_with_admin_user(self):
        pass

    def test_meetups_update_with_normal_user(self):
        pass

    def test_meetups_update_with_admin_user(self):
        pass

    def test_meetups_delete_with_normal_user(self):
        pass

    def test_meetups_delete_with_admin_user(self):
        pass


class TalksViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.list_view_name = 'talks:talks-list'
        self.detail_view_name = 'talks:talks-detail'
        self.upvote_view_name = 'talks:talks-upvote'
        self.downvote_view_name = 'talks:talks-downvote'

        self.serializer_class = TalkSerializer

        self.normal_user = User.objects.create(username='test', password='pass')
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@admin.com', password='s3cr3t'
        )

        self.meetup = Meetup.objects.create(date=datetime.now().date())
        self.talk = Talk.objects.create(
            meetup=self.meetup,
            author=self.normal_user,
            topic='test topic',
            description='test description'
        )

    def test_talks_list_with_anonymous_user(self):
        pass

    def test_talks_list_with_authenticated_user(self):
        pass

    def test_talks_detail_with_anonymous_user(self):
        pass

    def test_talks_detail_with_authenticated_user(self):
        pass

    def test_talks_create_with_anonymous_user(self):
        pass

    def test_talks_create_with_authenticated_user(self):
        pass

    def test_talks_update_with_anonymous_user(self):
        pass

    def test_talks_update_with_non_author_user(self):
        pass

    def test_talks_update_with_author_user(self):
        pass

    def test_talks_upvote_with_anonymous_user(self):
        pass

    def test_talks_upvote_with_authenticated_user(self):
        pass

    def test_talks_downvote_with_anonymous_user(self):
        pass

    def test_talks_downvote_with_authenticated_user(self):
        pass

    def test_talks_destroy_with_anonymous_user(self):
        pass

    def test_talks_destroy_with_normal_user(self):
        pass

    def test_talks_destroy_with_admin_user(self):
        pass
