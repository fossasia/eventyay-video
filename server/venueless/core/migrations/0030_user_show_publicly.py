# Generated by Django 3.0.6 on 2020-09-01 21:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0029_auditlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="show_publicly",
            field=models.BooleanField(default=True),
        ),
    ]
