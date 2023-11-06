# Generated by Django 4.2.6 on 2023-11-06 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("backend", "Back-end"),
                            ("frontend", "Front-end"),
                            ("ios", "iOS"),
                            ("android", "Android"),
                        ],
                        max_length=50,
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Authored_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]