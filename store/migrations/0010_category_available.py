# Generated by Django 5.0.1 on 2024-02-18 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_remove_plat_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
