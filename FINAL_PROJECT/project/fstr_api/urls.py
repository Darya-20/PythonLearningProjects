from django.urls import path
from django.urls import include, path
from .views import *

# submitData getPass updatePass getUserPasses


urlpatterns = [
    path('', submit_data, name='submit-data'),
]
