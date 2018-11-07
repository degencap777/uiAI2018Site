from django.contrib import admin
from django_summernote import admin as summernote_admin

from blog import models


class PostAdmin(summernote_admin.SummernoteModelAdmin):
    list_display = ['title', 'date', 'comment_count']
    search_fields = ['title', 'text']
    summernote_fields = ['text']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'post', 'approved']


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
