import logging
from collections import defaultdict
from datetime import timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...models import Post

"""logger = logging.getLogger(__name__)

def send_weekly_newslettert():
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
            html_content = render_to_string(
                'email_messages/weekly_newsletter.html', {
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
    

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Sends a weekly newsletter with new posts."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        scheduler.add_job(
            send_weekly_newslettert,
            trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),
            id="send_weekly_newslettert",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_newslettert'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")"""

