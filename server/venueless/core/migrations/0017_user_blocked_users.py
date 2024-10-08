# Generated by Django 3.0.6 on 2020-07-11 15:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_bbbcall_bbbserver"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="blocked_users",
            field=models.ManyToManyField(
                related_name="_user_blocked_users_+",
                to="core.User",
                symmetrical=False,
            ),
        ),
    ]
