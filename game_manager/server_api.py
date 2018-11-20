import requests

from uiai2018_site.settings import GAME_RUNNER_SERVERS


def get_server_status(server_address):
    r = requests.get('{}/api/server/status/'.format(server_address))
    return r.content


def request_game_run(client1_name, client1_path, client1_language,
                     client2_name, client2_path, client2_language):
    game_server = None
    for server in GAME_RUNNER_SERVERS:
        if get_server_status(server)['code'] == 200:
            game_server = server
            break
    if game_server is None:
        return False
    print(game_server)
