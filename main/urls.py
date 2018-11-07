from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from main.views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/get_settings/', get_settings, name='get_settings'),
    path('api/signup/', sign_up, name='sign_up'),
    path('api/user/info/', get_user_info, name='get_user_info'),
    path('api/user/edit/', edit_user_info, name='edit_user_info'),
    path('api/team/create/', create_team, name='create_team'),
    path('api/team/info/', get_team_info, name='get_team_info'),
    path('api/team/invite/', send_team_invitation, name='send_team_invitation'),
    path('api/team/reject/', reject_team_invitation, name='reject_team_invitation'),
    path('api/team/accept/', accept_team_invitation, name='accept_team_invitation'),
    path('api/team/leave/', leave_team, name='leave_team'),
]
