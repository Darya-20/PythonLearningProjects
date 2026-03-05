from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, UserProfileView, upgrade_me


urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
    path('user_profile/', UserProfileView.as_view(template_name = 'sign/user_profile.html'), name='user_profile'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
]

