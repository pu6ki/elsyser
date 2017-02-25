from django.contrib import admin

from students.models import Class, Subject, Student, Teacher, Grade


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'clazz']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject']


class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'student', 'subject']


admin.site.register(Class)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Grade, GradeAdmin)
