from django.core.management import BaseCommand

from game_manager.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        reqs = GameRequest.objects.filter(is_hidden=True)
        if input("Delete {} requests? [y/n] ").lower() == 'y':
            reqs.delete()
            print("Deleted")
