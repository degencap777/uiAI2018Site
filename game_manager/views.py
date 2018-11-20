from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.decorators import api_view

from game_manager.models import *
from user_panel.models import *
from user_panel.decorators import team_required
from game_manager import tasks


@api_view(['POST'])
@team_required
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
    game = Game(request=game_request)
    game.save()
    tasks.add_game_to_queue(game.pk)
    return Response({'message': 'درخواست بازی تایید شد.'}, status=HTTP_201_CREATED)


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
def callback_update_game_status(request):
    pass  # todo
