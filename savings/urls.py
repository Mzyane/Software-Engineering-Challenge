from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('create-goal/', views.create_goal, name='create_goal'),
    path('contribute/', views.contribute, name='contribute'),
    path('progress/', views.progress, name='progress'),
]
