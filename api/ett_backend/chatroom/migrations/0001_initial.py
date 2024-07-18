# Generated by Django 5.0.7 on 2024-07-17 12:46

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(null=True)),
                ("chat_room_uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("chat_room_name", models.CharField(default="My Chat Room", max_length=255)),
                ("analyze_target_name", models.CharField(max_length=255, null=True)),
                ("analyze_target_relation", models.CharField(max_length=255, null=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
