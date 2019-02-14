from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from app import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Ensure the root user password matches that in the config,
        or create it if it doesn't exist yet.
        """
        try:
            root_user = get_user_model().objects.get(
                username=settings.ROOT_USERNAME
            )
            root_user.set_password(
                settings.ROOT_PASSWORD
            )
        except ObjectDoesNotExist:
            get_user_model().objects.create_superuser(
                settings.ROOT_USERNAME,
                settings.ROOT_EMAIL,
                settings.ROOT_PASSWORD
            )
