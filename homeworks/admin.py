from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Homework, Submission


class SubmissionInline(admin.StackedInline):
    model = Submission


@register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    fields = ('topic', ('subject', 'clazz'), 'deadline', 'details', 'author')
    list_display = ('id', 'topic', 'subject', 'clazz', 'deadline', 'author')
    date_hierarchy = 'deadline'
    list_filter = ('subject', 'clazz', 'author')
    inlines = [
        SubmissionInline,
    ]
