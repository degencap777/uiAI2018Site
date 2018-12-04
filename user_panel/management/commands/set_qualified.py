from django.core.management import BaseCommand

from user_panel.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        teams = [code.team for code in Code.objects.filter(is_final=True)]
        for team in teams:
            print('{}: {}'.format(team.pk, team.name))
            team.qualified = True
            team.save()
