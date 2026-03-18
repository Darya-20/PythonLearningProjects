from django.urls import path
from django.urls import path
from .views import *


urlpatterns = [
    path('', submit_data, name='submit_data'),
    path('<int:pk>/', pass_detail, name='pass_detail'),
    path('<int:pk>/', update_pass, name='update_pass'),
    path('', list_by_user_email, name='list_by_user_email'),
]
