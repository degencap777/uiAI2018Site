from django.urls import path

from game_manager import views

urlpatterns = [
    path('send/', views.send_game_request, name='send_game_request'),
    path('accept/', views.accept_game_request, name='accept_game_request'),
    path('reject/', views.reject_game_request, name='reject_game_request'),
    path('callback/', views.callback_update_game_status, name='callback_game_status'),
]
