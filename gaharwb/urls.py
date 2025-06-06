from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('request-collaboration/', views.request_collaboration, name='request_collaboration'),
    path('request_thank_you/', views.request_thank_you, name='request_thank_you'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('about/', views.contact, name='about'),
    path('members/', views.team_members , name='members'),
    path('verify/<int:collab_id>/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/<int:collab_id>/', views.resend_otp_view, name='resend_otp'),
]