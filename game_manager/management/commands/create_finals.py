import time
import random

from django.core.management import BaseCommand
from django.urls import reverse

from uiai2018_site.settings import TEST_TEAM_PKS
from user_panel.models import *
from game_manager.models import *
from game_manager import tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        teams = Team.objects.filter(payment_verified=True)
        teams = sorted(teams, key=lambda t: t.pk)
        print('{} TEAMS\nID\tNAME'.format(len(teams)), '\n'.join(('{}\t{}'.format(t.pk, t.name) for t in teams)))
        while True:
            print("Enter id1 id2")
            id1, id2 = map(int, input().split())
            t1 = Team.objects.get(pk=id1)
            t2 = Team.objects.get(pk=id2)
            name = input("Enter game name: ")
            req = GameRequest.objects.create(sender=t1, receiver=t2, status=GameRequest.ACCEPTED, is_hidden=True)
            game = Game.objects.create(
                request=req,
                token="FINALS-{}-{}".format(req.pk, random.randint(10000, 100000)),
                game_type=Game.FINALS,
                finals_game_name=name,
            )
            print("ADDED {}: {} vs {}".format(game.pk, game.get_request_sender_team().name,
                                              game.get_request_receiver_team().name))
