from django.db import models

from students.models import Student


class News(models.Model):
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=10000, blank=False)
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    last_edited_on = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-last_edited_on']
        verbose_name_plural = 'news'
        unique_together = ('title', 'content')


    def __str__(self):
        return '{} ({})'.format(self.title, self.posted_on.date())


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField(max_length=2048)
    posted_on = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    last_edited_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '{} - {}'.format(self.posted_by, self.news)
