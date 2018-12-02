from background_task import background

from game_manager.models import Game
from game_manager.server_api import request_game_run


@background
def add_game_to_queue(game_id, callback_url):
    game = Game.objects.get(pk=game_id)
    success, message, code = request_game_run(
        client1_name=game.get_request_sender_team().name,
        client1_language=game.get_request_sender_team().get_final_code().language,
        client1_path=game.get_request_sender_team().get_final_code().code_zip.path,
        client2_name=game.get_request_receiver_team().name,
        client2_language=game.get_request_receiver_team().get_final_code().language,
        client2_path=game.get_request_receiver_team().get_final_code().code_zip.path,
        game_id=game.pk,
        token=game.token,
        callback_url='http://' + callback_url,
    )
    game.status_text = message
    if success:
        game.status = Game.PLAYING
    elif code == -2:
        game.status = Game.ERROR
    elif code == -1:
        game.status = Game.WAITING
        add_game_to_queue(game_id, callback_url, schedule=240)
    game.save()
    return success
