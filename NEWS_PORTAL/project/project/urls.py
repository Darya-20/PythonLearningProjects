from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news_portal.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
]
