from django.contrib import admin

from .models import Class, Student, Subject, Exam, News

admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(News)
