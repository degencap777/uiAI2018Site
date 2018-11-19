from functools import wraps
from rest_framework.status import *
from rest_framework.response import Response


def team_required(view):
    def decorator(request, *args, **kwargs):
        if not request.user.team:
            return Response({'message': 'شما در تیمی عضو نیستید.'}, status=HTTP_404_NOT_FOUND)
        response = view(request, *args, **kwargs)
        return response

    return wraps(view)(decorator)
