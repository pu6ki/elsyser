from django.contrib import admin

from .models import Class, Student, Subject, Exam, News, Homework, Comment


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'clazz']


admin.site.register(Class)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(News)
admin.site.register(Homework)
admin.site.register(Comment)
