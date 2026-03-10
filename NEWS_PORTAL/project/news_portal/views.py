from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .filters import PostFilter
from .forms import PostForm
from .models import *


class PostsList(ListView):
    model= Post
    ordering = '-datetime_creation'
    template_name = 'news_portal/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.categories_list = post.categories_post()
        return context
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    

class PostSearchList(PostsList):
    template_name = 'news_portal/posts_search.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoriesListView(ListView):
    model = Category
    ordering = ''
    template_name = 'news_portal/categories_list.html'
    context_object_name = 'categories'

    def get_absolute_url(self):
        return reverse('posts_category_list', kwargs={'pk': self.pk})


@login_required
def subsсribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubsсribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))


class PostsCategoriesListView(PostsList):
    template_name = 'news_portal/posts_category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['category'] = category
        return context
    
    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        return Post.objects.filter(categories=self.category).order_by('-datetime_creation')


class PostDetail(DetailView):
    model = Post
    template_name = 'news_portal/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = context['post'].categories_post()
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_portal/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return create_or_update(context, self.request.path)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        if 'article' in self.request.path:
            post.type = 'AR'
        else:
            post.type = 'NE'
        
        post.save()
        form.save_m2m()
        
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_portal/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return create_or_update(context, self.request.path)
    

class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news_portal.delete_post', )
    model = Post
    context_object_name = 'post'
    template_name = 'news_portal/post_delete.html'
    success_url = reverse_lazy('posts')


def create_or_update(context, path):
    if 'create' in path:
        title = 'Создание'
    else:
        title = 'Редактирование'
    if 'article' in path:
        title += ' статьи'
    else:
        title += ' новости'
    context['create_or_update'] = title
    return context
