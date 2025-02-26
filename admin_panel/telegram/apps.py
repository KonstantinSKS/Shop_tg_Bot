from django.apps import AppConfig


# class TelegramConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'telegram'

class TelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel.telegram'
    verbose_name = 'список пользователей Telegram'
