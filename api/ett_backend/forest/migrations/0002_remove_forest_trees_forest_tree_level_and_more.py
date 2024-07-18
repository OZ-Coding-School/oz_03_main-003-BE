# Generated by Django 5.0.7 on 2024-07-18 09:20

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forest", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="forest",
            name="trees",
        ),
        migrations.AddField(
            model_name="forest",
            name="tree_level",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="forest",
            name="forest_uuid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name="forest",
            name="user",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
