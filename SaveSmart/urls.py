"""
URL configuration for SaveSmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from savings import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('savings/', include('savings.urls', namespace='savings')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  
    path('create-goal/', views.create_goal, name='create_goal'),
    path('contribute/', views.contribute, name='contribute'),
    path('progress/', views.progress_view, name='progress'),
    path('goal/<int:pk>/', views.goal_detail, name='goal_detail'),
    path('update_goal/<int:pk>/', views.update_goal, name='update_goal'),
    path('delete_goal/<int:pk>/', views.delete_goal, name='delete_goal'),
    path('success/', views.success, name='success'),
]

