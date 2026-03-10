from django.apps import AppConfig


class NewsPortalConfig(AppConfig):
    name = 'news_portal'

    def ready(self):
        import news_portal.signals