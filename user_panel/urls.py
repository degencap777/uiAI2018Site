from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user_panel.views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/', include('rest_framework.urls')),
    path('get_settings/', get_settings, name='get_settings'),
    path('signup/', sign_up, name='sign_up'),
    path('user/info/', get_user_info, name='get_user_info'),
    path('user/edit/', edit_user_info, name='edit_user_info'),
    path('team/create/', create_team, name='create_team'),
    path('team/info/', get_team_info, name='get_team_info'),
    path('team/invite/', send_team_invitation, name='send_team_invitation'),
    path('team/reject/', reject_team_invitation, name='reject_team_invitation'),
    path('team/accept/', accept_team_invitation, name='accept_team_invitation'),
    path('team/leave/', leave_team, name='leave_team'),

]
