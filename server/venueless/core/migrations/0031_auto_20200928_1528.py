# Generated by Django 3.0.8 on 2020-09-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0030_user_show_publicly"),
    ]

    operations = [
        migrations.AddField(
            model_name="exhibitorlink",
            name="sorting_priority",
            field=models.IntegerField(default=0),
        ),
    ]
