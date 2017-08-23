from django.db import models
from django.contrib.auth.models import User

from students.models import Class


class BaseAbstractPost(models.Model):
    posted_on = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractPost(BaseAbstractPost):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class News(AbstractPost):
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=10000, blank=False)
    class_number = models.IntegerField(
        default=8,
        validators=[Class.CLASS_NUMBER_VALIDATORS],
        choices=Class.CLASS_NUMBERS
    )
    class_letter = models.CharField(
        max_length=1,
        blank=True,
        choices=Class.CLASS_LETTERS
    )

    def __str__(self):
        return '{} ({})'.format(self.title, self.posted_on.date())

    class Meta:
        ordering = ['-last_edited_on']
        verbose_name_plural = 'news'


class Comment(AbstractPost):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    author_image = models.URLField(blank=True)
    content = models.TextField(max_length=2048)

    def __str__(self):
        return '{} - {}'.format(self.author, self.news)

    class Meta:
        ordering = ['-posted_on']
