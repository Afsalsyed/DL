# urls.py
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views 
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from oss.views import Draftview
from dl.views import bridge

urlpatterns = [
    path('',register, name='register'),
    path('login/', login_view, name='login'),
    path('user_management/', user_management, name='user_management'),
    path('search-users/', search_users, name='search_users'),
    path('create_user/', create_user, name='create_user'),
    path('get_journals/', get_journals, name='get_journals'),
    path('assign_journal/', assign_journal, name='assign_journal'),
    path('fetch-groups/', fetch_groups, name='fetch_groups'),
    path('update-user-groups/', update_user_groups, name='update_user_groups'),
    path('reset_user_password/', reset_user_password, name='reset_user_password'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('set_new_password/<uidb64>/<token>/', set_new_password, name='set_new_password'),
    path('registration_complete/',registration_complete, name='registration_complete'),
    path('home/', home, name='home'),  # URL for a general page
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('user-management/',user_management, name='user_management'),
    path('assign-journal/', assign_journal, name='assign_journal'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    #logout
    path('logout/',custom_logout, name='logout'),
    #login redirect
    path('', Draftview, name='draft'),
    #dl
    path('', bridge, name='bridge'),
]
 