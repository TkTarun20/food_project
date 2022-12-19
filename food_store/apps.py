from django.apps import AppConfig


class FoodStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'food_store'

    def ready(self) -> None:
        import food_store.signals.handlers
