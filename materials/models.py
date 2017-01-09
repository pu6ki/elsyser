from django.db import models

from students.models import Subject, Teacher


class Material(models.Model):
    title = models.CharField(max_length=150, blank=True)
    section = models.CharField(max_length=150, blank=True)
    content = models.TextField(blank=False)
    class_number = models.IntegerField(choices=[(i, i) for i in range(8, 13)])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    video_url = models.URLField(blank=True)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return '{} - {} ({} class) posted by {}'.format(
            self.title, self.subject, self.class_number, self.author
        )
