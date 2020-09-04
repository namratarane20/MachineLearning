# Generated by Django 2.2.6 on 2019-12-20 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0005_auto_20191220_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionnaireTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorname', models.CharField(max_length=1000)),
                ('sectionname', models.CharField(max_length=1000)),
                ('controlname', models.CharField(max_length=1000)),
                ('securityquestion', models.CharField(max_length=1000)),
                ('response', models.CharField(max_length=1000)),
                ('additionalcomment', models.CharField(max_length=1000)),
                ('tagName', models.CharField(max_length=1000)),
            ],
        ),
        migrations.DeleteModel(
            name='TagsData',
        ),
    ]