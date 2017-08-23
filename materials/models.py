from django.db import models

from students.models import Subject, Teacher, Class


class Material(models.Model):
    title = models.CharField(max_length=150, blank=True)
    section = models.CharField(max_length=150, blank=True)
    content = models.TextField(blank=False)
    class_number = models.IntegerField(
        choices=Class.CLASS_NUMBERS,
        validators=[Class.CLASS_NUMBER_VALIDATORS]
    )
    subject = models.ForeignKey(Subject, related_name='materials', on_delete=models.CASCADE)
    video_url = models.URLField(blank=True)
    author = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} ({} class) posted by {}'.format(
            self.title, self.subject, self.class_number, self.author
        )
