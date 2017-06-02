from django.db import models

from students.models import Class, Subject, Teacher, Student
from news.models import Post


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    deadline = models.DateField(auto_now=False)
    details = models.TextField(max_length=256, blank=True)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)


    class Meta:
        ordering = ['-deadline', 'clazz', 'subject']

    def __str__(self):
        return '{} ({}) - {}'.format(self.subject, self.clazz, self.deadline)


class Submission(Post):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField(max_length=2048)
    solution_url = models.URLField(blank=True)
    checked = models.BooleanField(default=False)


    class Meta:
        ordering = ['-posted_on', '-last_edited_on']

    def __str__(self):
        return '{} - {} ({})'.format(self.student, self.homework, self.posted_on)
