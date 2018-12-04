import requests
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from uiai2018_site.settings import PAYMENT_API_KEY, PAYMENT_AMOUNT, TEST_TEAM_PKS
from user_panel.decorators import *
from user_panel.models import Team


@api_view(['POST'])
@team_required
@final_code_required
def begin_transaction(request):
    team = request.user.team
    factor_number = 'UIAI2018-{}'.format(team.pk)
    data = {
        'api': PAYMENT_API_KEY,
        'amount': PAYMENT_AMOUNT if team.pk not in TEST_TEAM_PKS else 1000,
        'redirect': 'http://acm.ui.ac.ir/uiai2018/api/payment/callback/',
        'mobile': request.user.phone,
        'factorNumber': factor_number,
        'description': 'ثبت‌نام در دومین دوره مسابقات چالش هوش مصنوعی دانشگاه اصفهان',
    }
    try:
        payment_request = requests.post('https://pay.ir/payment/send', data)
        response = payment_request.json()
        if response['status'] == 1:
            team.transaction_id1 = response['transId']
            team.factor_number = factor_number
            team.payment_message = 'درخواست پرداخت با موفقیت ارسال شد. لطفا در صفحه درگاه، پرداخت را تکمیل کنید.'
            team.save()
            return Response({
                'message': 'لطفا پرداخت را در صفحه درگاه تکمیل کنید.',
                'transaction_id': response['transId'],
                'factor_number': factor_number,
                'redirect_url': 'https://pay.ir/payment/gateway/{}'.format(response['transId']),
            }, status=HTTP_200_OK)
        else:
            team.payment_message = 'خطای {}: {}'.format(response['errorCode'], response['errorMessage'])
            team.save()
            return Response({'message': response['errorMessage']}, status=HTTP_400_BAD_REQUEST)
    except requests.exceptions.RequestException as err:
        team.payment_message = str(err)
        team.save()
        return Response({'message': 'خطا در اتصال به درگاه پرداخت.'}, status=HTTP_502_BAD_GATEWAY)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        status = request.POST['status']
        if status == 0:
            return render(request, 'payment_done.html', {'error': True, 'message': request.POST['message']})
        transaction_number = request.POST['transId']
        factor_number = request.POST['factorNumber']
        card_number = request.POST['cardNumber']
        trace_number = request.POST['traceNumber']
        team = Team.objects.get(factor_number=factor_number)
        if team.payment_verified or team.transaction_id2 is not None:
            message = 'پرداخت شما تایید شده'
            return render(request, 'payment_done.html', {'error': True, 'message': message})
        team.transaction_id2 = transaction_number
        team.card_number = card_number
        team.trace_number = trace_number
        team.payment_message = 'پرداخت شما انجام شد و در انتظار تایید می‌باشد.'
        team.save()
        try:
            verify_data = {'api': PAYMENT_API_KEY, 'transId': int(team.transaction_id2)}
            verify_request = requests.post('https://pay.ir/payment/verify', verify_data)
            response = verify_request.json()
            if response['status'] == 1:
                team.payment_amount = response['amount']
                team.payment_message = 'پرداخت با موفقیت انجام شد.' + \
                                       ' (شماره فاکتور: {} و کد رهگیری: {})'.format(team.factor_number,
                                                                                    team.trace_number)
                team.payment_verified = True
                team.save()
                return render(request, 'payment_done.html', {'message': team.payment_message})
            else:
                return render(request, 'payment_done.html', {'error': True, 'message': response['errorMessage']})
        except requests.exceptions.RequestException as err:
            return render(request, 'payment_done.html', {'error': True, 'message': str(err)})
    else:
        return redirect(reverse('dashboard'))
