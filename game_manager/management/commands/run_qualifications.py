import random
from time import time

from django.core.management import BaseCommand
from django.urls import reverse

from user_panel.models import *
from game_manager.models import *
from game_manager import tasks


class Command(BaseCommand):

    @staticmethod
    def run_game(id):
        tasks.add_game_to_queue(id, 'acm.ui.ac.ir/' + reverse('callback_game_status'))

    def handle(self, *args, **options):
        teams = [code.team for code in Code.objects.filter(is_final=True)]
        print('TEAMS\nID\tNAME', '\n'.join(('{}\t{}'.format(t.pk, t.name) for t in teams)))
        if input("Create games? [y/n]").lower() != 'y':
            return
        games = []
        for t1 in teams:
            for t2 in teams:
                if t1 != t2:
                    req = GameRequest.objects.create(sender=t1, receiver=t2, is_hidden=True)
                    token = 'QUAL{}-{}-{}'.format(req.pk, int(time()), random.randint(100000, 1000000))
                    game = Game.objects.create(request=req, token=token)
                    pass
