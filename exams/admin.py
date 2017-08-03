from django.contrib import admin

from .models import Exam


class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'date', 'clazz', 'topic', 'author')
    date_hierarchy = 'date'
    list_filter = ('subject', 'clazz', 'author')

admin.site.register(Exam, ExamAdmin)
