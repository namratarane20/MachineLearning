# Generated by Django 2.2.7 on 2020-01-20 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0004_search'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelevantData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywordColumn', models.CharField(max_length=30)),
                ('count', models.IntegerField()),
            ],
        ),
    ]
