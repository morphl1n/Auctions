# Generated by Django 4.1.3 on 2022-11-22 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='active',
        ),
    ]