from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    
    def __str__(self):
        return '{}{}'.format(self.number, self.title)

class Subject(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.title
