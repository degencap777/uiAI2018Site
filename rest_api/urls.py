from django.urls import path, include

from rest_api.views import *

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('get_settings/', get_settings, name='get_settings'),
]
