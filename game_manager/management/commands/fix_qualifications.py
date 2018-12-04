import time

from django.core.management import BaseCommand
from django.urls import reverse

from game_manager.models import *
from game_manager import server_api, tasks
from game_manager.server_api import request_game_run


class Command(BaseCommand):
    def handle(self, *args, **options):
        games = Game.objects.filter(game_type=Game.QUALIFICATION, status=Game.PLAYING)
        for i, game in enumerate(games):
            if i % 8 == 7:
                print('WAITING...')
                time.sleep(30)
            print('RUNNING {}: {} vs {}'.format(game.pk, game.get_request_sender_team().name,
                                                game.get_request_receiver_team().name))
            request_game_run(
                client1_name=game.get_request_sender_team().name,
                client1_language=game.get_request_sender_team().get_final_code().language,
                client1_path=game.get_request_sender_team().get_final_code().code_zip.path,
                client2_name=game.get_request_receiver_team().name,
                client2_language=game.get_request_receiver_team().get_final_code().language,
                client2_path=game.get_request_receiver_team().get_final_code().code_zip.path,
                game_id=game.pk,
                token=game.token,
                callback_url='http://' + 'acm.ui.ac.ir/' + reverse('callback_game_status'),
            )
