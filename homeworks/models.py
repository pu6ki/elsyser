from django.db import models

from students.models import Class, Subject, Teacher, Student

from news.models import BaseAbstractPost


class Homework(models.Model):
    topic = models.CharField(default='Homework', max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    deadline = models.DateField(auto_now=False)
    details = models.TextField(max_length=256, blank=True)
    author = models.ForeignKey(Teacher, null=True, related_name='homeworks', on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({}) - {}'.format(self.topic, self.subject, self.clazz)

    class Meta:
        ordering = ['-deadline', 'clazz', 'subject']


class Submission(BaseAbstractPost):
    homework = models.ForeignKey(Homework, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='submissions', on_delete=models.CASCADE)
    content = models.TextField(max_length=2048)
    solution_url = models.URLField(blank=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {} ({})'.format(self.student, self.homework, self.posted_on)

    class Meta:
        ordering = ['-posted_on', '-last_edited_on']
