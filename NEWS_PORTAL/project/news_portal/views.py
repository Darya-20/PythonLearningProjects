from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *
from .filters import PostFilter
from .forms import PostForm


class PostsList(ListView):
    model= Post
    ordering = '-datetime_creation'
    template_name = 'posts.html'
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
    template_name = 'posts_search.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = context['post'].categories_post()
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return create_or_update(context, self.request.path)

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'article' in self.request.path:
            post.type = 'article'
        else:
            post.type = 'news'
        return super().form_valid(form)
    

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return create_or_update(context, self.request.path)
    

class PostDelete(DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


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
