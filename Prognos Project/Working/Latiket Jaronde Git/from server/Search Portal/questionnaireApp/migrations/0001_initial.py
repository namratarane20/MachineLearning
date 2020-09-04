# Generated by Django 3.0 on 2020-01-23 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=30)),
                ('count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TagWithInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorname', models.CharField(max_length=1000)),
                ('sectionname', models.CharField(max_length=1000)),
                ('controlname', models.CharField(max_length=1000)),
                ('securityquestion', models.CharField(max_length=1000)),
                ('response', models.CharField(max_length=1000)),
                ('additionalcomment', models.CharField(max_length=1000)),
                ('tagName', models.CharField(max_length=1000)),
                ('tagDescription', models.CharField(max_length=1000)),
                ('flag', models.IntegerField(default=1)),
                ('dateTime', models.DateTimeField(auto_now=True)),
                ('userName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]