from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Post


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.order_by('name'),
        widget=forms.SelectMultiple(attrs={'size': 5}),
        label='Категории'
    )
    
    class Meta:
        model = Post
        fields = ['categories', 'title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10
            })
        }
        labels = {
            'title': 'Заголовок',
            'text': 'Текст'
        }
        
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 100:
            raise ValidationError({
                "text": "Текст не может быть менее 100 символов."
            })
        
        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичным заголовку."
            )

        return cleaned_data