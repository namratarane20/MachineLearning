# Generated by Django 3.0 on 2020-02-12 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0009_auto_20200211_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='admindb',
            name='status',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
