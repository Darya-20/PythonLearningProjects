from django import forms
from django_filters import FilterSet, DateFilter
from .models import Post


class PostFilter(FilterSet):
    datetime_creation = DateFilter(
        field_name='datetime_creation',
        lookup_expr='gte',
        label='Показать публикации позже ',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'categories': ['exact'],
        }