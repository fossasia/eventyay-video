# Generated by Django 3.2.3 on 2021-06-01 19:39

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0046_alter_janusserver_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("content", models.TextField()),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("open", "Open"),
                            ("closed", "Closed"),
                            ("archived", "Archived"),
                        ],
                        default="draft",
                        max_length=8,
                    ),
                ),
                (
                    "poll_type",
                    models.CharField(
                        choices=[
                            ("choice", "Choice"),
                            ("multi", "Multi Choice"),
                        ],
                        default="choice",
                        max_length=6,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("is_pinned", models.BooleanField(default=False)),
                ("cached_results", models.JSONField(blank=True, null=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polls",
                        to="core.room",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PollOption",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("order", models.IntegerField(default=1)),
                ("content", models.TextField()),
                (
                    "poll",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="options",
                        to="core.poll",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="PollVote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="votes",
                        to="core.polloption",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="poll_votes",
                        to="core.user",
                    ),
                ),
            ],
            options={
                "unique_together": {("option", "sender")},
            },
        ),
    ]
