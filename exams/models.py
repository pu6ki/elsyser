from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from datetime import datetime

# TODO: Update database

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Subject(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        ordering = ['title', 'teacher']

    def __str__(self):
        return self.title


class Class(models.Model):
    number = models.PositiveSmallIntegerField(
        default=8,
        validators=[MinValueValidator(8), MaxValueValidator(12)]
    )
    title = models.CharField(
        max_length=1,
        choices=(
            ('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G')
        )
    )

    class Meta:
        ordering = ['number', 'title']

    def __str__(self):
        return '{}{}'.format(self.number, self.title)


class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    topic = models.CharField(max_length=60)

    class Meta:
        ordering = ['date', 'subject', 'clazz']

    def clean(self):
        if self.date < datetime.now().date():
            raise ValidationError('Only future dates allowed.')
        if self.date.weekday() not in range(0, 5):
            raise ValidationError('Exam can be done only from Monday to Friday.')


    def __str__(self):
        return '{} - {} ({})'.format(
            self.subject,
            self.clazz,
            self.date.strftime('%d-%m-%Y')
        )
