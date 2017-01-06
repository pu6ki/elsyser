from django.contrib import admin

from students.models import (
    Class, Student, Subject, Exam, News,
    Homework, Comment, Material, Submission, Teacher
)


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'clazz']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class ExamAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'date', 'clazz', 'topic', 'author']
    date_hierarchy = 'date'


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'posted_on']
    date_hierarchy = 'posted_on'


class HomeworkAdmin(admin.ModelAdmin):
    fields = (('subject', 'clazz'), 'deadline', 'details', 'author')
    list_display = ['id', 'subject', 'clazz', 'deadline', 'author']
    date_hierarchy = 'deadline'


class CommentAdmin(admin.ModelAdmin):
    fields = ('news', 'posted_by', 'content')
    list_display = ['id', 'news', 'content', 'posted_by', 'posted_on']
    date_hierarchy = 'posted_on'


class MaterialAdmin(admin.ModelAdmin):
    fields = (
        ('title', 'section'), 'content',
        ('class_number', 'subject'),
        'video_url',
        'author'
    )
    list_display = [
        'id', 'title', 'section', 'class_number', 'subject', 'author'
    ]


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'homework', 'student']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject']


admin.site.register(Class)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Teacher, TeacherAdmin)
