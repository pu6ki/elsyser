from django.contrib import admin
from django.contrib.admin.decorators import register

from materials.admin import MaterialInline

from .models import Class, Subject, Student, Teacher, Grade


@register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    inlines = [
        MaterialInline
    ]


class GradeInline(admin.TabularInline):
    model = Grade


@register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clazz')
    exclude = ('activation_key',)
    inlines = [
        GradeInline
    ]


@register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject')
    exclude = ('activation_key',)


@register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'student', 'subject')
    list_filter = ('student', 'subject')

admin.site.register(Class)
