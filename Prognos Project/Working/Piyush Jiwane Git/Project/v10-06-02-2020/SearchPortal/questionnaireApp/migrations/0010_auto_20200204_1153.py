# Generated by Django 2.2.6 on 2020-02-04 06:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0009_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagwithinfo',
            name='createdBy',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tagwithinfo',
            name='destroyedBY',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tagwithinfo',
            name='updatedBy',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
