from django.db import models

from main.models import User


class Post(models.Model):
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=1024)
    text = models.TextField(max_length=8192)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.all().count()

    @property
    def approved_comment_count(self):
        return self.get_approved_comments().count()

    def get_approved_comments(self):
        return self.comments.filter(approved=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.user.get_full_name(), self.post.title)
