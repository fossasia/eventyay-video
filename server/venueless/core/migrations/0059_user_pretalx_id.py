# Generated by Django 3.2.14 on 2022-07-19 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0058_auto_20220302_0946"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="pretalx_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]