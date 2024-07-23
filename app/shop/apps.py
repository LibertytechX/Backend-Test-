from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self) -> None:
        from shop.signals import reduce_product_stock_on_save, increase_product_stock_on_delete
