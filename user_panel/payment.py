import requests
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from uiai2018_site.settings import PAYMENT_API_KEY, PAYMENT_AMOUNT, TEST_TEAM_PKS
from user_panel.decorators import *
from user_panel.models import *


@api_view(['POST'])
@team_required
@final_code_required
def begin_transaction(request):
    discount_code = request.data['discount_code']
    discount_percent = 0
    if discount_code:
        try:
            discount = DiscountCode.objects.get(code=discount_code)
            if discount.team_used is not None:
                return Response({'این کد تخفیف قبلاً استفاده شده.'}, status=HTTP_403_FORBIDDEN)
            discount_percent = discount.discount_percent
        except DiscountCode.DoesNotExist:
            return Response({'کد تخفیف مورد نظر موجود نمی‌باشد.'}, status=HTTP_404_NOT_FOUND)
    team = request.user.team
    factor_number = 'UIAI2018-{}'.format(team.pk)
    if discount_percent > 0:
        factor_number += '-{}'.format(discount_code)
    data = {
        'api': PAYMENT_API_KEY,
        'amount': int(PAYMENT_AMOUNT * (100 - discount_percent) // 100) if team.pk not in TEST_TEAM_PKS else 1000,
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
            if discount_percent > 0:
                team.payment_message += ' (کد تخفیف {} درصد: {})'.format(discount_percent, discount_code)
            team.save()
            return Response({
                'message': team.payment_message,
                'transaction_id': response['transId'],
                'factor_number': factor_number,
                'redirect_url': 'https://pay.ir/payment/gateway/{}'.format(response['transId']),
                'discount_percent': discount_percent,
            })
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
                team.payment_message = 'پرداخت با موفقیت انجام شد.'
                team.payment_verified = True
                team.save()
                if factor_number.count('-') == 2:
                    discount_code = factor_number.split('-')[-1]
                    discount = DiscountCode.objects.get(code=discount_code)
                    discount.team_used = team
                    discount.save()
                return redirect(reverse('dashboard'))
            else:
                return render(request, 'payment_done.html', {'error': True, 'message': response['errorMessage']})
        except requests.exceptions.RequestException as err:
            return render(request, 'payment_done.html', {'error': True, 'message': str(err)})
    else:
        return redirect(reverse('dashboard'))
