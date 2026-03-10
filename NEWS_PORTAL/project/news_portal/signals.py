from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Category, Post

@receiver(m2m_changed, sender=Post.categories.through)
def message_subscribers(sender, instance, action, pk_set, **kwargs):
    if action != 'post_add':
        return
    
    categories = Category.objects.filter(id__in=pk_set)
    
    for category in categories:
        subscribers = category.subscribers.all()

        for user in subscribers:
            html_content = render_to_string(
                'email_messages/new_post_message.html', {
                    'post': instance,
                    'category': category,
                    'user': user,
                }
            )

            send_mail(
                subject=instance.title,
                message=f'Здравствуй, {user.username}. Новая публикация в твоём любимом разделе!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
                html_message=html_content,
            )
