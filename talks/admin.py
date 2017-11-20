from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Meetup, Talk


class TalkInline(admin.StackedInline):
    model = Talk


@register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')
    date_hierarchy = 'date'
    list_filter = ('date',)
    inlines = [TalkInline]
