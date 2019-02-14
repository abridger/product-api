from django.core.management.base import BaseCommand
import os
from products.tasks import import_products


class Command(BaseCommand):
    def handle(self, *args, **options):
        fixtures_directory = os.path.join(
            os.path.dirname(__file__),
            '../../../fixtures'
        )
        import_products(fixtures_directory)
