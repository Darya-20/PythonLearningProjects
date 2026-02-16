from django.urls import path
from .views import * 


urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('search/', PostSearchList.as_view(), name='posts_search'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]