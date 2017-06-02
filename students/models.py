from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Subject(models.Model):
    title = models.CharField(unique=True, max_length=50)


    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.URLField(
        default='http://elsyser.herokuapp.com/static/default.png', blank=False
    )
    info = models.TextField(max_length=2048, blank=True)


    class Meta:
        abstract = True


class Student(Account):
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)


    def __str__(self):
        return '{} ({})'.format(self.user.username, self.clazz)


class Teacher(Account):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.user.username, self.subject)


class Grade(models.Model):
    value = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(6)])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} ({})'.format(self.student, self.subject, self.value)
