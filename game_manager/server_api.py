import requests

from uiai2018_site.settings import GAME_RUNNER_SERVERS


def get_server_status(server_address):
    r = requests.get('{}/api/server/status/'.format(server_address))
    return r.json()


def get_best_server():
    for server in GAME_RUNNER_SERVERS:
        print(get_server_status(server))
        if get_server_status(server)['code'] == 200:
            return server


def request_game_run(client1_name, client1_path, client1_language,
                     client2_name, client2_path, client2_language):
    game_server = get_best_server()

