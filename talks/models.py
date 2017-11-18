from django.db import models
from django.contrib.auth.models import User

from vote.models import VoteModel


class Talk(VoteModel):
    author = models.ForeignKey(User, related_name='talks', on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    date = models.DateField()
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.__class__.__name__, self.topic)

    class Meta:
        ordering = ['vote_score', 'date']
