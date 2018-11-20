from background_task import background

from game_manager.models import Game


@background
def add_game_to_queue(game_id):
    game = Game.objects.get(pk=game_id)
