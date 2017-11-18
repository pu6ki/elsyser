from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Talk


@register(Talk)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'date')
    date_hierarchy = 'date'
    list_filter = ('topic', 'date', 'author')
