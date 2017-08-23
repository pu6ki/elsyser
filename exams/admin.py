from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Exam


@register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'date', 'clazz', 'topic', 'author')
    date_hierarchy = 'date'
    list_filter = ('subject', 'clazz', 'author')
