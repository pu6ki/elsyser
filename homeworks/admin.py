from django.contrib import admin

from .models import Homework, Submission


class SubmissionInline(admin.StackedInline):
    model = Submission


class HomeworkAdmin(admin.ModelAdmin):
    fields = (('subject', 'clazz'), 'deadline', 'details', 'author')
    list_display = ('id', 'subject', 'clazz', 'deadline', 'author')
    date_hierarchy = 'deadline'
    list_filter = ('subject', 'clazz', 'author')
    inlines = [
        SubmissionInline
    ]

admin.site.register(Homework, HomeworkAdmin)
