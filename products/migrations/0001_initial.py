# Generated by Django 2.1.7 on 2019-02-14 14:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('gtin', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category_1', models.CharField(max_length=255)),
                ('category_2', models.CharField(max_length=255)),
                ('category_3', models.CharField(max_length=255)),
                ('energy_100g', models.IntegerField(blank=True, null=True)),
                ('energy_serving', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
