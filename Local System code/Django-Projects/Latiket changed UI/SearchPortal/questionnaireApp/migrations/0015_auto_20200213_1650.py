# Generated by Django 3.0 on 2020-02-13 16:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0014_auto_20200213_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admindb',
            name='receivedDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='admindb',
            name='submittedDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
