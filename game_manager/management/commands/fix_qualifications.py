import time

from django.core.management import BaseCommand
from django.urls import reverse

from game_manager.models import *
from game_manager import server_api, tasks


class Command(BaseCommand):
    def handle(self, *args, **options):
        games = Game.objects.filter(game_type=Game.QUALIFICATION, status=Game.PLAYING)
        for i, game in enumerate(games):
            t = (i // 8) * 10
            print('t = {}; {}: {} vs {}'.format(t, game.pk, game.get_request_sender_team().name,
                                               game.get_request_receiver_team().name))
            tasks.add_game_to_queue(game.pk, 'acm.ui.ac.ir/' + reverse('callback_game_status'), schedule=t)
