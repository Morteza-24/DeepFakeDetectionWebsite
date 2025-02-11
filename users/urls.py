from django.urls import path
from .views import (
    home_view, signin_view, signup_view, profile_view, 
    profile_edit_view, logout_view, 
    password_reset_view, password_reset_done_view, 
    password_reset_confirm_view, password_reset_complete_view)#,set_language_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', signin_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('logout/', logout_view, name='logout'),
    # path('set_language/', set_language_view, name='set_language'),


    # Password reset URLs
    path('password-reset/', 
         password_reset_view, 
         name='password_reset'),
    path('password-reset/done/', 
         password_reset_done_view, 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         password_reset_confirm_view, 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         password_reset_complete_view, 
         name='password_reset_complete'),
]