# Generated by Django 5.0.7 on 2024-07-25 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatroom", "0005_remove_chatroom_analyze_target_name"),
        ("dialog", "0007_alter_aidialog_user_dialog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdialog",
            name="chat_room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="user_dialog", to="chatroom.chatroom"
            ),
        ),
    ]
