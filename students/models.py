from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_date


class Class(models.Model):

    number = models.IntegerField(
        validators=[MinValueValidator(8), MaxValueValidator(12)],
        choices=[(i, i) for i in range(8, 13)],
    )
    title = models.CharField(
        max_length=1,
        choices=[(l, l) for l in ['A', 'B', 'V', 'G']],
    )

    class Meta:
        ordering = ['number', 'title']
        verbose_name_plural = 'classes'


    def __str__(self):
        return '{}{}'.format(self.number, self.title)


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.user.username, self.clazz)


class Subject(models.Model):

    title = models.CharField(unique=True, max_length=50)

    class Meta:
        ordering = ['title']


    def __str__(self):
        return self.title


class Exam(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, validators=[validate_date])
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    topic = models.CharField(unique=True, max_length=60)

    class Meta:
        ordering = ['date', 'subject', 'clazz']


    def __str__(self):
        return '{} - {} ({})'.format(
            self.subject,
            self.clazz,
            self.date
        )


class News(models.Model):

    title = models.CharField(max_length=50)
    content = models.TextField(max_length=2048)
    date = models.DateField(auto_now=True)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', 'title', 'clazz']
        verbose_name_plural = 'news'


    def __str__(self):
        return '{} ({}) - {}'.format(
            self.title,
            self.date,
            self.clazz
        )
