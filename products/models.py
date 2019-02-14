import uuid
from django.db import models


class Product(models.Model):
    """Product model

    The main model to store information about products. This currently contains
    fields that would eventually be moved to separate, related entities.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    gtin = models.CharField(
        max_length=255
    )
    # The brand is stored as a field on the product here, but would eventually
    # be given its own model and linked to products through a Forein Key
    # relationship.
    brand = models.CharField(
        max_length=255
    )
    description = models.TextField()
    # Categories stored as separate fields here, since all products seem to
    # have three separate categories, and the requirement was to use a single
    # database table. Eventually, a category would form a separate model, and
    # be referenced here by a Foriegn Key field.
    category_1 = models.CharField(
        max_length=255
    )
    category_2 = models.CharField(
        max_length=255
    )
    category_3 = models.CharField(
        max_length=255
    )
    energy_100g = models.IntegerField(
        blank=True,
        null=True
    )
    energy_serving = models.IntegerField(
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=255
    )
    updated_at = models.DateTimeField(
        blank=True,
        null=True
    )
