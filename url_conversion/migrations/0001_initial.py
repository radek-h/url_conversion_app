# Generated by Django 3.2.18 on 2023-05-18 09:26

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="URL",
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
                ("full_url", models.URLField()),
                ("url_shorten_key", models.CharField(max_length=5)),
            ],
        ),
    ]