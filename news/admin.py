from django.contrib import admin

from news.models import News, Comment


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'posted_on']
    date_hierarchy = 'posted_on'


class CommentAdmin(admin.ModelAdmin):
    fields = ('news', 'posted_by', 'content')
    list_display = ['id', 'news', 'content', 'posted_by', 'posted_on']
    date_hierarchy = 'posted_on'

admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
