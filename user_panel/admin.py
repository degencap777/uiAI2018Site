from django.contrib import admin

from user_panel.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email', 'phone', 'institute', 'team']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'institute', 'team']
    list_filter = ['institute', 'team']
    fields = ['first_name', 'last_name', 'email', 'phone', 'institute', 'team']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_member1', 'get_member2', 'get_member3']
    search_fields = ['name']


admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Settings)
