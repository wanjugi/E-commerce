# Generated by Django 4.2.4 on 2023-08-20 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='Active',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='ImageUrl',
            new_name='imageUrl',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='Price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='Title',
            new_name='title',
        ),
    ]
