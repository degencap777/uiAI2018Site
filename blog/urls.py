from django.urls import path

from blog import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('post/<int:pk>/', views.view_post, name='view_post'),
]
