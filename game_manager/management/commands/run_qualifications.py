import time
import random

from django.core.management import BaseCommand
from django.urls import reverse

from user_panel.models import *
from game_manager.models import *
from game_manager import tasks


class Command(BaseCommand):

    @staticmethod
    def run_games(games: list):
        for i, game in enumerate(games):
            if i % 7 == 8:
                time.sleep(10)
            tasks.add_game_to_queue(game.pk, 'acm.ui.ac.ir/' + reverse('callback_game_status'))

    def handle(self, *args, **options):
        test_ids = [29, 39, 74, 75]
        teams = [code.team for code in Code.objects.filter(is_final=True) if code.team.pk not in test_ids]
        teams = sorted(teams, key=lambda t: t.pk)
        print('{} TEAMS\nID\tNAME'.format(len(teams)), '\n'.join(('{}\t{}'.format(t.pk, t.name) for t in teams)))
        if input("Create games? [y/n] ").lower() != 'y':
            return
        reqs = []
        games = []
        i = 0
        for i1 in range(0, len(teams)):
            for i2 in range(i1 + 1, len(teams)):
                t1, t2 = teams[i1], teams[i2]
                i += 1
                print('{}: {} vs {}'.format(i, t1.name, t2.name))
                req = GameRequest.objects.create(sender=t1, receiver=t2, is_hidden=True)
                reqs.append(req)
                token = 'QUAL{}-{}-{}'.format(req.pk, int(time.time()), random.randint(100000, 1000000))
                games.append(Game.objects.create(request=req, token=token, game_type=Game.QUALIFICATION))
        if input("Run games? [y/n] ").lower() != 'y':
            return
        Command.run_games(games)
