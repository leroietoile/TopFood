# Generated by Django 5.0.1 on 2024-02-08 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]