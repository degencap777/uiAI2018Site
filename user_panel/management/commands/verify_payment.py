import requests
from django.core.management import BaseCommand

from uiai2018_site.settings import PAYMENT_API_KEY


class Command(BaseCommand):

    def handle(self, *args, **options):
        transaction_id = int(input("Enter transaction ID: "))
        data = {
            "api": PAYMENT_API_KEY,
            "transId": transaction_id
        }
        response = requests.post('https://pay.ir/payment/verify', data=data)
        print('Response Code: {}'.format(response.status_code))
        print('Response Data: {}'.format(response.json()))
