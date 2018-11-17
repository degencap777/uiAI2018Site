from django.contrib import admin

from user_panel.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'english_full_name', 'email', 'phone', 'institute', 'team']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'institute', 'team', 'english_full_name']
    list_filter = ['institute', 'team']
    fields = ['first_name', 'last_name', 'english_full_name', 'email', 'phone', 'institute', 'team',
              'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_member1', 'get_member2', 'get_member3']
    search_fields = ['name']


class CodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'compilation_status', 'upload_timestamp', 'is_final']
    list_filter = ['compilation_status', 'is_final']


admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Settings)
admin.site.register(Code, CodeAdmin)
