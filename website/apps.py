from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'website'
class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'