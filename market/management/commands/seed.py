from django.core.management.base import BaseCommand

from market.seed import seed


class Command(BaseCommand):
    help = "Load demo users and listings"

    def handle(self, *args, **options):
        seed()
        self.stdout.write("Seeded.")
