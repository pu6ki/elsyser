from django.contrib import admin

from exams.models import Exam


class ExamAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'date', 'clazz', 'topic', 'author']
    date_hierarchy = 'date'


admin.site.register(Exam, ExamAdmin)
