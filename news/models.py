from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    posted_on = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class News(Post):
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=10000, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    class_number = models.IntegerField(default=8)
    class_letter = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.title, self.posted_on.date())

    class Meta:
        ordering = ['-last_edited_on']
        verbose_name_plural = 'news'


class Comment(Post):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    author_image = models.URLField(blank=True)
    content = models.TextField(max_length=2048)

    def __str__(self):
        return '{} - {}'.format(self.posted_by, self.news)

    class Meta:
        ordering = ['-posted_on']
