# Generated by Django 2.2.6 on 2019-12-30 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0009_auto_20191228_1247'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TagsData',
            new_name='TagWithInfo',
        ),
    ]
