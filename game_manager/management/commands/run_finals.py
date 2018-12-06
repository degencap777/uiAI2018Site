import requests

from django.core.management import BaseCommand
from django.urls import reverse

from game_manager.models import *
from uiai2018_site.settings import GAME_RUNNER_SERVERS


def request_game_run(game_server, client1_name, client1_path, client1_language,
                     client2_name, client2_path, client2_language,
                     game_id, token, callback_url):
    if game_server is None:
        return False, 'سروری برای اجرای بازی پیدا نشد.', -1
    files = {'team1_code': open(client1_path, 'rb'), 'team2_code': open(client2_path, 'rb')}
    data = {'team1_name': client1_name, 'team1_language': client1_language,
            'team2_name': client2_name, 'team2_language': client2_language,
            'game_id': game_id, 'token': token, 'callback_url': callback_url}
    r = requests.post('{}/api/game/request/'.format(game_server), files=files, data=data)
    return r


class Command(BaseCommand):
    def handle(self, *args, **options):
        games = Game.objects.filter(game_type=Game.FINALS, status=Game.WAITING)
        server_index = 1
        for i, game in enumerate(games):
            if i % 4 == 0:
                server_index = int(input("Server number? [9/10] "))
                server_index -= 8
            print('RUNNING {}: {} vs {}'.format(game.pk, game.get_request_sender_team().name,
                                                game.get_request_receiver_team().name))
            request_game_run(
                game_server=GAME_RUNNER_SERVERS[server_index],
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
