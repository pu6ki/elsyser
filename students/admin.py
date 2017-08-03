from django.contrib import admin

from materials.admin import MaterialInline

from .models import Class, Subject, Student, Teacher, Grade


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    inlines = [
        MaterialInline
    ]


class GradeInline(admin.TabularInline):
    model = Grade


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'clazz']
    exclude = ('activation_key',)
    inlines = [
        GradeInline
    ]


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject']
    exclude = ('activation_key',)


class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'student', 'subject']

admin.site.register(Class)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Grade, GradeAdmin)
