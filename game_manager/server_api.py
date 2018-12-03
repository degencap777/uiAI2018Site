import requests

from uiai2018_site.settings import GAME_RUNNER_SERVERS


def get_best_server(for_compile=False):
    best_server, count = None, 8
    for server in GAME_RUNNER_SERVERS:
        try:
            r = requests.get('{}/api/server/status/'.format(server), params={'for_compile': for_compile})
            if r.status_code == 200 and int(r.json()['running_count']) < count:
                best_server = server
        except BaseException:
            pass
    return best_server


def request_game_run(client1_name, client1_path, client1_language,
                     client2_name, client2_path, client2_language,
                     game_id, token, callback_url):
    game_server = get_best_server()
    if game_server is None:
        return False, 'سروری برای اجرای بازی پیدا نشد.', -1
    files = {'team1_code': open(client1_path, 'rb'), 'team2_code': open(client2_path, 'rb')}
    data = {'team1_name': client1_name, 'team1_language': client1_language,
            'team2_name': client2_name, 'team2_language': client2_language,
            'game_id': game_id, 'token': token, 'callback_url': callback_url}
    r = requests.post('{}/api/game/request/'.format(game_server), files=files, data=data)
    if r.status_code == 201:
        return True, 'بازی برای اجرا به سرور شماره {} ارسال شد.'.format(GAME_RUNNER_SERVERS.index(game_server)), 0
    else:
        return False, 'خطا در ارسال بازی به سرور: {}'.format(r.text), -2
