from django.shortcuts import render
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from main.models import *


@api_view(['GET'])
@permission_classes([AllowAny])
def get_settings(request):
    return Response(dict((s.key, s.value) for s in Settings.objects.all()))


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    try:
        User.objects.create_user(
            email=request.data.get('email'),
            password=request.data.get('password'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            phone=request.data.get('phone'),
            institute=request.data.get('institute'),
            english_full_name=request.data.get('english_full_name')
        )
        return Response({'message': 'ثبت‌نام با موفقیت انجام شد.'}, status=HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_info(request):
    user = request.user
    return Response(user.get_dict())


@api_view(['POST'])
def edit_user_info(request):
    try:
        request.user.email = request.data.get('email')
        request.user.first_name = request.data.get('first_name')
        request.user.last_name = request.data.get('last_name')
        request.user.phone = request.data.get('phone')
        request.user.institute = request.data.get('institute')
        request.user.english_full_name = request.data.get('english_full_name')
        request.user.save()
        return Response({'message': 'اطلاعات شما ویرایش شد.'})
    except ValidationError as e:
        return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_team(request):
    if request.user.team is not None:
        return Response({'message': 'شما در یک تیم عضو هستید و نمی‌توانید تیم جدیدی ایجاد کنید.'},
                        status=HTTP_403_FORBIDDEN)
    team_name = request.data.get('name')
    if not team_name:
        return Response({'message': 'نام تیم نمی‌تواند خالی باشد.'}, status=HTTP_400_BAD_REQUEST)
    team = Team(name=team_name)
    team.save()
    request.user.team = team
    request.user.save()
    return Response({'message': 'تیم {} با موفقیت ساخته شد.'.format(team.name)}, status=HTTP_201_CREATED)


@api_view(['GET'])
def get_team_info(request):
    if not request.user.team:
        return Response({'message': 'شما در تیمی عضو نیستید.'}, status=HTTP_404_NOT_FOUND)
    return Response(request.user.team.get_dict())


@api_view(['POST'])
def send_team_invitation(request):
    if not request.user.team:
        return Response({'message': 'شما در تیمی عضو نیستید.'}, status=HTTP_404_NOT_FOUND)
    receiver_email = request.data.get('email')
    try:
        receiver = User.objects.get(email=receiver_email)
        TeamInvitation(
            sender=request.user,
            receiver=receiver,
            team=request.user.team,
        ).save()
        return Response({'message': 'دعوت‌نامه به کاربر مورد نظر ارسال شد.'}, status=HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'message': 'کاربر با ایمیل مورد نظر پیدا نشد.'}, status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
def accept_team_invitation(request):
    if request.user.team is not None:
        return Response({'message': 'شما در یک تیم عضو هستید و نمی‌توانید دعوت‌نامه‌ای را بپذیرید.'},
                        status=HTTP_403_FORBIDDEN)
    invitation_id = request.data.get('id')
    if not invitation_id or not str(invitation_id).isdecimal():
        return Response({'message': 'شماره دعوت‌نامه اشتباه است.'}, status=HTTP_400_BAD_REQUEST)
    try:
        invitation = TeamInvitation.objects.get(pk=int(invitation_id))
    except TeamInvitation.DoesNotExist:
        return Response({'message': 'دعوت‌نامه مورد نظر یافت نشد.'}, status=HTTP_404_NOT_FOUND)
    if invitation.receiver != request.user:
        return Response({'message': 'این دعوت‌نامه مربوط به شما نیست.'}, status=HTTP_403_FORBIDDEN)
    if invitation.status != TeamInvitation.PENDING:
        return Response({'message': 'دعوت‌نامه فاقد اعتبار است.'}, status=HTTP_403_FORBIDDEN)
    request.user.team = invitation.team
    request.user.save()
    invitation.status = TeamInvitation.ACCEPTED
    invitation.save()
    return Response({'message': 'شما در تیم {} عضو شدید.'.format(invitation.team.name)})


@api_view(['POST'])
def reject_team_invitation(request):
    invitation_id = request.data.get('id')
    if not invitation_id or not str(invitation_id).isdecimal():
        return Response({'message': 'شماره دعوت‌نامه اشتباه است.'}, status=HTTP_400_BAD_REQUEST)
    try:
        invitation = TeamInvitation.objects.get(pk=int(invitation_id))
    except TeamInvitation.DoesNotExist:
        return Response({'message': 'دعوت‌نامه مورد نظر یافت نشد.'}, status=HTTP_404_NOT_FOUND)
    if invitation.receiver != request.user:
        return Response({'message': 'این دعوت‌نامه مربوط به شما نیست.'}, status=HTTP_403_FORBIDDEN)
    if invitation.status != TeamInvitation.PENDING:
        return Response({'message': 'دعوت‌نامه فاقد اعتبار است.'}, status=HTTP_403_FORBIDDEN)
    invitation.status = TeamInvitation.REJECTED
    invitation.save()
    return Response({'message': 'دعوت به عضویت در تیم {} رد شد.'.format(invitation.team.name)})


@api_view(['POST'])
def leave_team(request):
    if not request.user.team:
        return Response({'message': 'شما در تیمی عضو نیستید.'}, status=HTTP_404_NOT_FOUND)
    team_name = request.user.team.name
    request.user.team = None
    request.user.save()
    return Response({'message': 'عضویت شما در تیم {} لغو شد.'.format(team_name)})


def landing(request):
    return render(request, 'index.html')
