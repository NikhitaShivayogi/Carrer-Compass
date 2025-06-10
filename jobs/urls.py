from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.user_home, name='user_home'),

    path('job/', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('company/<int:company_id>/', views.company_profile, name='company_profile'),
    path('profile/', views.user_profile, name='user_profile'),

    path('signup/', views.signup, name='signup'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('applications/', views.my_applications, name='my_applications'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
