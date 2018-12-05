from django.contrib import admin

from user_panel.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'english_full_name', 'email', 'phone', 'institute', 'team']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'institute', 'team', 'english_full_name']
    list_filter = ['institute', 'team']
    fields = ['first_name', 'last_name', 'english_full_name', 'email', 'phone', 'institute', 'team',
              'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'wants_dorm']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_member1', 'get_member2', 'get_member3', 'qualified', 'payment_verified']
    search_fields = ['name']
    list_filter = ['qualified', 'payment_verified']


class CodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'compilation_status', 'upload_timestamp', 'is_final']
    list_filter = ['compilation_status', 'is_final']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'team_used']
    list_filter = ['discount_percent']
    search_fields = ['code', 'discount_percent']


admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Settings)
admin.site.register(Code, CodeAdmin)
admin.site.register(DiscountCode, DiscountAdmin)
