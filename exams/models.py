from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# TODO: Update database to have valid teacher for each Subject

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Subject(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1)

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

    class Meta:
        ordering = ['-date', 'subject', 'clazz']

    def __str__(self):
        return '{} - {} ({})'.format(
            self.subject,
            self.clazz,
            self.date.strftime('%d-%m-%Y')
        )
