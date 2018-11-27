from time import time
from datetime import datetime

from django.urls import reverse
from django.http import HttpResponse
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.sites.shortcuts import get_current_site

from game_manager.models import *
from user_panel.models import *
from user_panel.decorators import *
from game_manager import tasks


@api_view(['POST'])
@team_required
@final_code_required
def send_game_request(request):
    try:
        receiver = Team.objects.get(pk=int(request.data.get('team_id')))
    except ValueError:
        return Response({'message': 'شناسه تیم نامعتبر است.'}, status=HTTP_400_BAD_REQUEST)
    except Team.DoesNotExist:
        return Response({'message': 'تیم مورد نظر پیدا نشد.'}, status=HTTP_404_NOT_FOUND)
    sender = request.user.team
    game_request = GameRequest(sender=sender, receiver=receiver)
    game_request.save()
    return Response({'message': 'درخواست بازی دوستانه با موفقیت ارسال شد.'}, status=HTTP_201_CREATED)


@api_view(['POST'])
@team_required
@final_code_required
def accept_game_request(request):
    try:
        game_request = GameRequest.objects.get(pk=int(request.data.get('request_id')))
    except ValueError:
        return Response({'message': 'شناسه درخواست بازی نامعتبر است.'}, status=HTTP_400_BAD_REQUEST)
    except GameRequest.DoesNotExist:
        return Response({'message': 'درخواست مورد نظر پیدا نشد.'}, status=HTTP_404_NOT_FOUND)
    if request.user.team != game_request.receiver:
        return Response({'message': 'شما قادر به تایید این بازی نیستید.'}, status=HTTP_403_FORBIDDEN)
    game_request.status = GameRequest.ACCEPTED
    game_request.save()
    game = Game(request=game_request, token=str(int(time())))
    game.save()
    success = tasks.add_game_to_queue(game.pk, str(get_current_site(request)) + reverse('callback_game_status'))
    if success:
        return Response({'message': 'درخواست بازی تایید شد.'}, status=HTTP_201_CREATED)
    else:
        return Response({'message': 'تایید درخواست با خطا مواجه شد.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@team_required
def reject_game_request(request):
    try:
        game_request = GameRequest.objects.get(pk=int(request.data.get('request_id')))
    except ValueError:
        return Response({'message': 'شناسه درخواست بازی نامعتبر است.'}, status=HTTP_400_BAD_REQUEST)
    except GameRequest.DoesNotExist:
        return Response({'message': 'درخواست مورد نظر پیدا نشد.'}, status=HTTP_404_NOT_FOUND)
    if request.user.team != game_request.receiver:
        return Response({'message': 'شما قادر به رد این بازی نیستید.'}, status=HTTP_403_FORBIDDEN)
    game_request.status = GameRequest.REJECTED
    game_request.save()
    return Response({'message': 'درخواست بازی رد شد.'}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def callback_update_game_status(request):
    try:
        game = Game.objects.get(pk=int(request.data['game_id']))
    except Game.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    except ValueError:
        return Response(status=HTTP_400_BAD_REQUEST)
    game.logged_team1_name = request.data['team1_name']
    game.logged_team1_goals = request.data['team1_goals']
    game.logged_team2_name = request.data['team2_name']
    game.logged_team2_goals = request.data['team2_goals']
    game.log_file = request.data['log_file']
    game.status = Game.FINISHED
    game.run_date = datetime.now()
    game.save()
    return Response(status=HTTP_200_OK)


@api_view(['GET'])
def get_game_info(request):
    try:
        game = Game.objects.get(pk=int(request.data['game_id']))
    except ValueError:
        return Response({'message': 'شناسه بازی نامعتبر است.'}, status=HTTP_400_BAD_REQUEST)
    except Game.DoesNotExist:
        return Response({'message': 'بازی مورد نظر پیدا نشد.'}, status=HTTP_404_NOT_FOUND)
    if game.get_request_sender_team() == request.user.team or game.get_request_receiver_team() == request.user.team:
        return Response(game.get_dict())
    else:
        return Response({'message': 'شما اجازه مشاهده نتایج این بازی را ندارید.'}, status=HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_game_log(request):
    game_id = request.GET.get('game_id')
    token = request.GET.get('token')
    try:
        game = Game.objects.get(pk=int(game_id))
    except Game.DoesNotExist:
        return Response("Game not found", status=HTTP_404_NOT_FOUND)
    except ValueError:
        return Response("ID format incorrect", status=HTTP_400_BAD_REQUEST)
    if not game.log_file:
        return Response("Game has no log file", status=HTTP_404_NOT_FOUND)
    if game.token != token:
        return Response("Invalid token", status=HTTP_401_UNAUTHORIZED)
    with open(game.log_file.path, 'r') as lf:
        log_text = lf.read()
    return HttpResponse(log_text)
