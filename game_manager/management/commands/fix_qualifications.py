import time

from django.core.management import BaseCommand
from django.urls import reverse

from game_manager.models import *
from game_manager import server_api


class Command(BaseCommand):
    def handle(self, *args, **options):
        games = Game.objects.filter(game_type=Game.QUALIFICATION, status=Game.PLAYING)
        i = 0
        for game in games:
            if i % 8 == 7:
                time.sleep(10)
            print('RUNNING {}: {} vs {}'.format(game.pk, game.get_request_sender_team().name,
                                                game.get_request_receiver_team().name))
            ok, msg, code = server_api.request_game_run(
                client1_name=game.get_request_sender_team().name,
                client1_language=game.get_request_sender_team().get_final_code().language,
                client1_path=game.get_request_sender_team().get_final_code().code_zip.path,
                client2_name=game.get_request_receiver_team().name,
                client2_language=game.get_request_receiver_team().get_final_code().language,
                client2_path=game.get_request_receiver_team().get_final_code().code_zip.path,
                game_id=game.pk,
                token=game.token,
                callback_url='http://acm.ui.ac.ir/' + reverse('callback_game_status'),
            )
            if ok:
                print('{}: {}'.format(game.pk, msg))
            else:
                print('WAITING: {}'.format(code))
                time.sleep(10)
