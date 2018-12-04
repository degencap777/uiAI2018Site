from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user_panel.views import *
from user_panel import payment

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/', include('rest_framework.urls')),
    path('get_settings/', get_settings, name='get_settings'),
    path('get_version/', get_version, name='get_version'),
    path('signup/', sign_up, name='sign_up'),
    path('user/info/', get_user_info, name='get_user_info'),
    path('user/edit/', edit_user_info, name='edit_user_info'),
    path('team/create/', create_team, name='create_team'),
    path('team/info/', get_team_info, name='get_team_info'),
    path('team/invite/', send_team_invitation, name='send_team_invitation'),
    path('team/reject/', reject_team_invitation, name='reject_team_invitation'),
    path('team/accept/', accept_team_invitation, name='accept_team_invitation'),
    path('team/leave/', leave_team, name='leave_team'),
    path('team/upload_code/', upload_code, name='upload_code'),
    path('team/set_final_code/', set_final_code, name='set_final_code'),
    path('get_available_teams/', get_available_teams, name='get_available_teams'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('get_statistics/', get_statistics, name='get_stats'),
    path('payment/begin/', payment.begin_transaction, name='pay_init'),
    path('payment/callback/', payment.callback, name='pay_callback'),
    path('user/request_dorm/', request_dorm, name='request_dorm'),
]
