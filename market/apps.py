from django.apps import AppConfig


class MarketConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "market"

    def ready(self):
        from django.db.models.signals import post_migrate

        def _seed(sender, **kwargs):
            from market.seed import seed

            seed()

        post_migrate.connect(_seed, sender=self, dispatch_uid="market-seed")
