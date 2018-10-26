from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_api.models import *


@api_view(['GET'])
def get_settings(request):
    return Response(dict((s.key, s.value) for s in Settings.objects.all()))


@api_view(['POST'])
def signup(request):
    pass


@api_view(['POST'])
def login(request):
    pass


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
