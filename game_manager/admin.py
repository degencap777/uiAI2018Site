from django.contrib import admin

from game_manager.models import *
from game_manager import tasks


def start_games(modeladmin, request, queryset):
    for game in queryset:
        tasks.add_game_to_queue(game.pk)


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
