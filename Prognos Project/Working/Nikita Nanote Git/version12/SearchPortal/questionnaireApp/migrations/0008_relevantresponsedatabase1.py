# Generated by Django 2.2.7 on 2020-02-10 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0007_auto_20200210_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelevantResponseDatabase1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_Keyword', models.CharField(max_length=60)),
                ('count', models.IntegerField()),
                ('keywordSearched', models.CharField(max_length=30)),
                ('db_user', models.CharField(max_length=30)),
            ],
        ),
    ]
