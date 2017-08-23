from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Class(models.Model):
    CLASS_NUMBERS = (
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
    )
    CLASS_NUMBER_VALIDATORS = [MinValueValidator(8), MaxValueValidator(12)]

    CLASS_LETTERS = (
        ('A', 'A'),
        ('B', 'B'),
        ('V', 'V'),
        ('G', 'G'),
    )

    number = models.IntegerField(validators=CLASS_NUMBER_VALIDATORS, choices=CLASS_NUMBERS)
    letter = models.CharField(max_length=1, choices=CLASS_LETTERS)

    def __str__(self):
        return '{}{}'.format(self.number, self.letter)

    class Meta:
        ordering = ['number', 'letter']
        verbose_name_plural = 'classes'


class Subject(models.Model):
    title = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.URLField(
        default='http://elsyser.herokuapp.com/static/default.png', blank=False
    )
    info = models.TextField(max_length=2048, blank=True)
    activation_key = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        abstract = True


class Student(Account):
    clazz = models.ForeignKey(Class, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.user.username, self.clazz)


class Teacher(Account):
    subject = models.ForeignKey(Subject, related_name='teachers', on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.user.username, self.subject)


class Grade(models.Model):
    GRADE_VALIDATORS = [MinValueValidator(2), MaxValueValidator(6)]

    value = models.FloatField(validators=GRADE_VALIDATORS)
    subject = models.ForeignKey(Subject, related_name='grades', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='grades', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} ({})'.format(self.student, self.subject, self.value)
