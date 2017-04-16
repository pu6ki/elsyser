from django.contrib import admin

from .models import Homework, Submission


class HomeworkAdmin(admin.ModelAdmin):
    fields = (('subject', 'clazz'), 'deadline', 'details', 'author')
    list_display = ['id', 'subject', 'clazz', 'deadline', 'author']
    date_hierarchy = 'deadline'


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'homework', 'student']

admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Submission, SubmissionAdmin)
