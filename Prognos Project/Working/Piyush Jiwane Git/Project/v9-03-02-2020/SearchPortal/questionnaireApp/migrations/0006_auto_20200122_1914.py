# Generated by Django 2.2.7 on 2020-01-22 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0005_relevantdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelevantResponseDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userKeyword', models.CharField(max_length=60)),
                ('count', models.IntegerField()),
                ('keywordSearched', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='RelevantData',
        ),
    ]
