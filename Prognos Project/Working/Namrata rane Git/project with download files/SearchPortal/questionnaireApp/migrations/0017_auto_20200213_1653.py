# Generated by Django 3.0 on 2020-02-13 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0016_auto_20200213_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admindb',
            name='receivedDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='admindb',
            name='submittedDate',
            field=models.DateTimeField(null=True),
        ),
    ]