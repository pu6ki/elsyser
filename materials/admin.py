from django.contrib import admin

from materials.models import Material


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


admin.site.register(Material, MaterialAdmin)
