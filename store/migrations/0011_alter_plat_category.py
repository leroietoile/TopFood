# Generated by Django 5.0.1 on 2024-02-19 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_category_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plat',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='store.category'),
        ),
    ]
