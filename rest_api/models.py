from os.path import join
from django.db import models
from django.contrib.auth.models import AbstractUser

from rest_api import upload_filenames


class User(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16)
    institute = models.CharField(max_length=64)
    social_id = models.CharField(max_length=16)
    team = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name='members', blank=True, null=True)

    def __str__(self):
        return self.get_full_name()


class Team(models.Model):
    name = models.CharField(max_length=32, unique=True)
    logo = models.ImageField(upload_to=upload_filenames.team_logo, default='default_team_logo.png')

    @property
    def member1(self):
        return self.members.all()[0] if self.members.count() > 0 else None

    @property
    def member2(self):
        return self.members.all()[1] if self.members.count() > 1 else None

    def member3(self):
        return self.members.all()[2] if self.members.count() > 2 else None

    def __str__(self):
        return self.name


class Settings(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    value = models.TextField(max_length=8192)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'
