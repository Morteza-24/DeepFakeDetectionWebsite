from django.urls import path
from .views import home_view, signin_view, signup_view, profile_view, profile_edit_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', signin_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('logout/', logout_view, name='logout'),
]