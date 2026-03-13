from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Category, Post

@shared_task
def message_subscribers_task(post_pk, category_pks, **kwargs):
    post = Post.objects.get(pk=post_pk)

    categories = Category.objects.filter(pk__in=category_pks)
    
    for category in categories:
        subscribers = category.subscribers.all()
        
        for user in subscribers:
            html_content = render_to_string(
                'email_messages/new_post_message.html', {
                    'post': post,
                    'category': category,
                    'user': user,
                }
            )
            
            kwargs = {
                'subject': post.title,
                'message': f'Здравствуй, {user.username}. Новая публикация в твоём любимом разделе!',
                'from_email': settings.DEFAULT_FROM_EMAIL,
                'recipient_list': [user.email],
                'fail_silently': True,
                'html_message': html_content
            }

            message_subscribers_task.delay(kwargs)
            
            send_mail(
                subject=post.title,
                message=f'Здравствуй, {user.username}. Новая публикация в твоём любимом разделе!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
                html_message=html_content,
            )


@shared_task
def send_weekly_newslettert_task():
    pass


from celery import shared_task
from collections import defaultdict
from datetime import timedelta
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post

logger = logging.getLogger(__name__)

@shared_task
def send_weekly_newsletter_task():
    week_ago = timezone.now() - timedelta(days=7)

    new_posts = Post.objects.filter(datetime_creation__gte=week_ago).prefetch_related('categories')

    if not new_posts.exists():
        logger.info("No new posts this week.")
        return

    category_posts = defaultdict(list)
    for post in new_posts:
        for category in post.categories.all():
            category_posts[category].append(post)

    for category, posts in category_posts.items():
        subscribers = category.subscribers.all()

        for user in subscribers:
            try:
                html_content = render_to_string(
                    'email_messages/weekly_newsletter.html',{
                        'user': user,
                        'category': category,
                        'posts': posts,
                    }
                )

                send_mail(
                    subject=f'Новые публикации за неделю в разделе "{category.name}"',
                    message=f'Здравствуй, {user.username}! В разделе "{category.name}" появились новые публикации за последнюю неделю',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                    html_message=html_content,
                )
                logger.info(f"Sent weekly digest to {user.email} for category {category.name}")

            except Exception as e:
                logger.error(f"Failed to send email to {user.email}: {str(e)}")

