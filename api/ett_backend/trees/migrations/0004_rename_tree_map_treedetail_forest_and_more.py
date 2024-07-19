# Generated by Django 5.0.7 on 2024-07-19 07:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trees", "0003_alter_treedetail_table"),
    ]

    operations = [
        migrations.RenameField(
            model_name="treedetail",
            old_name="tree_map",
            new_name="forest",
        ),
        migrations.RenameField(
            model_name="treedetail",
            old_name="tree_growth_level",
            new_name="tree_level",
        ),
        migrations.RemoveField(
            model_name="treedetail",
            name="anger",
        ),
        migrations.RemoveField(
            model_name="treedetail",
            name="happiness",
        ),
        migrations.RemoveField(
            model_name="treedetail",
            name="indifference",
        ),
        migrations.RemoveField(
            model_name="treedetail",
            name="location_x",
        ),
        migrations.RemoveField(
            model_name="treedetail",
            name="location_y",
        ),
        migrations.RemoveField(
            model_name="treedetail",
            name="sadness",
        ),
        migrations.RemoveField(
            model_name="treedetail",
            name="worry",
        ),
        migrations.AddField(
            model_name="treedetail",
            name="location",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="treedetail",
            name="tree_uuid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name="treedetail",
            name="tree_name",
            field=models.CharField(default="My Tree", max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name="TreeEmotion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(null=True)),
                ("happiness", models.DecimalField(decimal_places=1, max_digits=3)),
                ("anger", models.DecimalField(decimal_places=1, max_digits=3)),
                ("sadness", models.DecimalField(decimal_places=1, max_digits=3)),
                ("worry", models.DecimalField(decimal_places=1, max_digits=3)),
                ("indifference", models.DecimalField(decimal_places=1, max_digits=3)),
                ("tree", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="trees.treedetail")),
            ],
            options={
                "db_table": "tree_emotion",
            },
        ),
    ]
