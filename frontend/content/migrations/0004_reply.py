# Generated by Django 4.2 on 2024-03-07 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("content", "0003_rename_details_detail"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reply",
            fields=[
                ("reply_id", models.AutoField(primary_key=True, serialize=False)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "replied_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "replied_on",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="content.comment",
                    ),
                ),
            ],
        ),
    ]