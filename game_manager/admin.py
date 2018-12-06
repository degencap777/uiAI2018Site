from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from game_manager.models import *
from game_manager import tasks


def start_games(modeladmin, request, queryset):
    for game in queryset:
        tasks.add_game_to_queue(game.pk, str(get_current_site(request)) + reverse('callback_game_status'))


start_games.short_description = 'Start selected games'


def set_status_playing(modeladmin, request, queryset):
    for game in queryset:
        game.status = Game.PLAYING
        game.save()


set_status_playing.short_description = 'Set status to PLAYING'


def set_status_waiting(modeladmin, request, queryset):
    for game in queryset:
        game.status = Game.WAITING
        game.save()


set_status_waiting.short_description = 'Set status to WAITING'


def set_status_error(modeladmin, request, queryset):
    for game in queryset:
        game.status = Game.ERROR
        game.save()


set_status_error.short_description = 'Set status to ERROR'


class RequestAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'sender', 'receiver', 'status']
    list_filter = ['sender', 'receiver', 'status']
    search_fields = ['sender', 'receiver', 'status']


class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_request_sender_team', 'get_request_receiver_team', 'status', 'game_type',
                    'get_result_string', 'get_log_url']
    list_filter = ['status', 'game_type']
    actions = [start_games, set_status_playing, set_status_waiting, set_status_error]

    def get_log_link_html(self, obj):
        return "<a href={}>View Log</a>".format(obj.get_log_url())

    get_log_link_html.allow_tags = True


admin.site.register(GameRequest, RequestAdmin)
admin.site.register(Game, GameAdmin)
