from django.core.management import BaseCommand

from uiai2018_site.settings import TEST_TEAM_PKS
from user_panel.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        teams = Team.objects.filter(qualified=True, payment_verified=True)
        teams = sorted(teams, key=lambda t: t.name)
        print("TEAM NAME,PAYMENT VERIFIED,FIRST NAME,LAST NAME,EMAIL,PHONE,INSTITUTE")
        for team in teams:
            if team.pk not in TEST_TEAM_PKS:
                for member in team.members.all()[:3]:
                    print("{},{},{},{},{},{},{}".format(team.name, team.payment_verified, member.first_name,
                                                        member.last_name, member.email, member.phone, member.institute))
