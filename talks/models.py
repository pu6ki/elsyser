from django.db import models
from django.contrib.auth.models import User

from vote.models import VoteModel


class Meetup(models.Model):
    date = models.DateField()

    def __str__(self):
        return '{} ({})'.format(self.__class__.__name__, self.date)

    class Meta:
        ordering = ['date']


class Talk(VoteModel):
    meetup = models.ForeignKey(Meetup, related_name='talks', null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='talks', on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.__class__.__name__, self.topic)

    class Meta:
        ordering = ['vote_score']
