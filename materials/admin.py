from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Material


class MaterialInline(admin.StackedInline):
    model = Material


@register(Material)
class MaterialAdmin(admin.ModelAdmin):
    fields = (
        ('title', 'section'), 'content',
        ('class_number', 'subject'),
        'video_url',
        'author'
    )
    list_display = ('id', 'title', 'section', 'class_number', 'subject', 'author')
    list_filter = ('class_number', 'subject', 'author')
