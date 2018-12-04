import time
import random

from django.core.management import BaseCommand

from uiai2018_site.settings import TEST_TEAM_PKS
from user_panel.models import *
from game_manager.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        teams = [code.team for code in Code.objects.filter(is_final=True) if code.team.pk not in TEST_TEAM_PKS]
        teams = sorted(teams, key=lambda t: t.pk)
        print('{} TEAMS\nID\tNAME'.format(len(teams)), '\n'.join(('{}\t{}'.format(t.pk, t.name) for t in teams)))
        i = 0
        i1 = int(input("Enter team index: "))
        t1 = Team.objects.get(pk=i1)
        for i2 in range(0, len(teams)):
            if t1 != t1:
                t2 = teams[i2]
                i += 1
                print('{}: {} vs {}'.format(i, t1.name, t2.name))
                req = GameRequest.objects.create(sender=t1, receiver=t2, is_hidden=True)
                token = 'QUAL{}-{}-{}'.format(req.pk, int(time.time()), random.randint(100000, 1000000))
                Game.objects.create(request=req, token=token, game_type=Game.QUALIFICATION)
