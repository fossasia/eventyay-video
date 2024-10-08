# Generated by Django 3.0.6 on 2020-08-27 18:15

import django.contrib.postgres.fields.jsonb
from django.db import migrations

import venueless.core.models.world


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0027_room_schedule_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="world",
            name="feature_flags",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=venueless.core.models.world.default_feature_flags,
            ),
        ),
    ]
