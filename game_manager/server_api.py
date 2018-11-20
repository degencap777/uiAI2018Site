import requests

from uiai2018_site.settings import GAME_RUNNER_SERVERS


def get_best_server():
    for server in GAME_RUNNER_SERVERS:
        r = requests.get('{}/api/server/status/'.format(server))
        try:
            if r.json()['code'] == 200:
                return server
        except requests.exceptions.ConnectionError:
            pass


def request_game_run(client1_name, client1_path, client1_language,
                     client2_name, client2_path, client2_language):
    game_server = get_best_server()
    files = {'team1_code': open(client1_path, 'rb'), 'team2_code': open(client2_path, 'rb')}
    data = {'team1_name': client1_name, 'team1_language': client1_language,
            'team2_name': client2_name, 'team2_language': client2_language}
    r = requests.post('{}/api/game/request/'.format(game_server), files=files, data=data)
    print(r.json())
