from django.contrib import admin

from blog import models


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'comment_count']
    search_fields = ['title', 'text']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'post', 'approved']


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
