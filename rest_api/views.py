from django.contrib.auth import authenticate, login
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password

from rest_api.models import *


@api_view(['GET'])
def get_settings(request):
    return Response(dict((s.key, s.value) for s in Settings.objects.all()))


@api_view(['POST'])
def sign_up(request):
    try:
        validate_password(request.POST.get('password'))
        user = User.objects.create_user(
            username=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            institute=request.POST.get('institute'),
            social_id=request.POST.get('social_id'),
        )
        user.set_password(request.POST.get('password'))
        user.save()
        return Response(status=HTTP_201_CREATED)
    except BaseException as e:
        return Response(status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_info(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_team_request(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_user_info(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_team(request):
    pass


@login_required
def accept_invitation(request, invitation_id):
    pass
