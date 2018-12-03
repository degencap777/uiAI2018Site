from functools import wraps
from rest_framework.status import *
from rest_framework.response import Response

from uiai2018_site import settings


def team_required(view):
    def decorator(request, *args, **kwargs):
        if not request.user.team:
            return Response({'message': 'شما در تیمی عضو نیستید.'}, status=HTTP_404_NOT_FOUND)
        response = view(request, *args, **kwargs)
        return response

    return wraps(view)(decorator)


def final_code_required(view):
    def decorator(request, *args, **kwargs):
        if request.user.team.get_final_code() is None:
            return Response({'message': 'تیم شما کدی را به عنوان کد نهایی انتخاب نکرده است.'},
                            status=HTTP_403_FORBIDDEN)
        return view(request, *args, **kwargs)

    return wraps(view)(decorator)


def check_registration_deadline(view):
    def decorator(request, *args, **kwargs):
        if not settings.REGISTRATION_OPEN:
            return Response({'message': 'مهلت ثبت‌نام به پایان رسیده.'}, status=HTTP_410_GONE)

        return view(request, *args, **kwargs)

    return wraps(view)(decorator)


def check_upload_deadline(view):
    def decorator(request, *args, **kwargs):
        if not settings.UPLOAD_CODE_OPEN:
            return Response({'message': 'مهلت ارسال کد به پایان رسیده.'}, status=HTTP_410_GONE)
        return view(request, *args, **kwargs)

    return wraps(view)(decorator)
