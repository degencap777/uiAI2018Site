from django.contrib import admin

from game_manager.models import *


class RequestAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'sender', 'receiver', 'status']
    list_filter = ['sender', 'receiver', 'status']
    search_fields = ['sender', 'receiver', 'status']


class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_request_sender_team', 'get_request_receiver_team', 'status']
    list_filter = ['status']


admin.site.register(GameRequest, RequestAdmin)
admin.site.register(Game, GameAdmin)
