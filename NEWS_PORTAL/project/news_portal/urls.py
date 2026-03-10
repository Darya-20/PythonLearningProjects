from django.urls import path

from .views import *

urlpatterns = [
    path('', PostsList.as_view(template_name = 'news_portal/posts.html'), name='posts'),
    path('search/', PostSearchList.as_view(template_name = 'news_portal/posts_search.html'), name='posts_search'),
    path('categories/', CategoriesListView.as_view(template_name = 'news_portal/categories_list.html'), name='categories_list'),
    path('category/<int:pk>/subsсribe/', subsсribe, name='subsсribe'),
    path('category/<int:pk>/unsubsсribe/', unsubsсribe, name='unsubsсribe'),
    path('category/<int:pk>/', PostsCategoriesListView.as_view(template_name = 'news_portal/posts_category_list.html'), name='posts_category_list'),

    path('<int:pk>/', PostDetail.as_view(template_name = 'news_portal/post_detail.html'), name='post_detail'),
    path('news/create/', PostCreate.as_view(template_name = 'news_portal/post_edit.html'), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(template_name = 'news_portal/post_edit.html'), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(template_name = 'news_portal/post_delete.html'), name='news_delete'),
    path('article/create/', PostCreate.as_view(template_name = 'news_portal/post_edit.html'), name='article_create'),
    path('article/<int:pk>/edit/', PostUpdate.as_view(template_name = 'news_portal/post_edit.html'), name='article_edit'),
    path('article/<int:pk>/delete/', PostDelete.as_view(template_name = 'news_portal/post_delete.html'), name='article_delete'),
]