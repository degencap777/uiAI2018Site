from django.contrib import admin

from game_manager.models import *


def start_games(modeladmin, request, queryset):
    for game in queryset:
        game.send_to_server()


start_games.short_description = 'Start selected games'


class RequestAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'sender', 'receiver', 'status']
    list_filter = ['sender', 'receiver', 'status']
    search_fields = ['sender', 'receiver', 'status']


class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_request_sender_team', 'get_request_receiver_team', 'status']
    list_filter = ['status']
    actions = [start_games]


admin.site.register(GameRequest, RequestAdmin)
admin.site.register(Game, GameAdmin)
