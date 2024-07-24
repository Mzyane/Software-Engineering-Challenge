from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'savings'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('create-goal/', views.create_goal, name='create_goal'),
    path('contribution/<int:goal_id>/', views.contribute, name='contribution'),
    path('progress/', views.progress_view, name='progress_view'),
    path('goal/<int:pk>/', views.goal_detail, name='goal_detail'),
    path('update-goal/<int:pk>/', views.update_goal, name='update_goal'),
    path('delete-goal/<int:pk>/', views.delete_goal, name='delete_goal'),
    path('success/', views.success, name='success'),
    path('input/', views.input_financial_data, name='input_financial_data'),
    path('financial-insights/', views.financial_insights, name='financial_insights'),
]
