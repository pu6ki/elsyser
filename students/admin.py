from django.contrib import admin

from .models import Class, Student, Subject, Exam

admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Exam)
