from django.core.management import BaseCommand

from uiai2018_site.settings import TEST_TEAM_PKS
from user_panel.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        qualified_only = (input("Qualified only? [y/n] ").lower() == 'y')
        paid_only = False
        if qualified_only:
            paid_only = (input("Paid only? [y/n] ").lower() == 'y')
        teams = Team.objects.all()
        if qualified_only:
            teams = teams.filter(qualified=True)
        if paid_only:
            teams = teams.filter(payment_verified=True)
        teams = sorted(teams, key=lambda t: t.name)
        print("TEAM NAME,PAYMENT VERIFIED,FIRST NAME (1),LAST NAME (1),EMAIL (1),PHONE (1),INSTITUTE (1)," +
              "FIRST NAME (2),LAST NAME (2),EMAIL (2),PHONE (2), INSTITUTE (2)," +
              "FIRST NAME (3),LAST NAME (3),EMAIL (3),PHONE (3), INSTITUTE (3)")
        for team in teams:
            if team.pk not in TEST_TEAM_PKS:
                s = "{},{}".format(team.name, "YES" if team.payment_verified else "NO")
                for m in team.members.all()[:3]:
                    s += ",{},{},{},{},{}".format(m.first_name, m.last_name, m.email, m.phone, m.institute)
                print(s)
