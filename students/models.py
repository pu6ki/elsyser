from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from students.validators import validate_date

import os


def get_upload_path(instance, filename):
    _, file_extension = os.path.splitext(filename)

    return 'images/{}{}'.format(instance.user.username, file_extension)


class Class(models.Model):
    number = models.IntegerField(
        validators=[MinValueValidator(8), MaxValueValidator(12)],
        choices=[(i, i) for i in range(8, 13)],
    )
    letter = models.CharField(
        max_length=1,
        choices=[(l, l) for l in ['A', 'B', 'V', 'G']],
    )


    class Meta:
        ordering = ['number', 'letter']
        verbose_name_plural = 'classes'


    def __str__(self):
        return '{}{}'.format(self.number, self.letter)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to=get_upload_path, default='images/default.png'
    )
    info = models.TextField(max_length=2048, blank=True)


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
    details = models.TextField(max_length=1000, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    class Meta:
        ordering = ['date', 'subject', 'clazz']


    def __str__(self):
        return '{} - {} ({})'.format(self.subject, self.clazz, self.date)


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


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    deadline = models.DateField(auto_now=False)
    details = models.TextField(max_length=256, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    class Meta:
        ordering = ['-deadline', 'clazz', 'subject']


    def __str__(self):
        return '{} ({}) - {}'.format(self.subject, self.clazz, self.deadline)


class Material(models.Model):
    title = models.CharField(max_length=150, blank=True)
    section = models.CharField(max_length=150, blank=True)
    content = models.TextField(blank=False)
    class_number = models.IntegerField(choices=[(i, i) for i in range(8, 13)])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    video_url = models.URLField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return '{} - {} ({} class) posted by {}'.format(
            self.title, self.subject, self.class_number, self.author
        )


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField(max_length=2048)
    posted_on = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    last_edited_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '{} - {}'.format(self.posted_by, self.news)
