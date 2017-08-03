from django.contrib import admin

from .models import News, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    ordering = ('-last_edited_on',)


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'posted_on']
    date_hierarchy = 'posted_on'
    inlines = [
        CommentInline
    ]

admin.site.register(News, NewsAdmin)
