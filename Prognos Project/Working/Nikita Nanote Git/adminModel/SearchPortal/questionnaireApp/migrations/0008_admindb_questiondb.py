# Generated by Django 2.2.7 on 2020-02-11 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0007_auto_20200205_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorName', models.CharField(max_length=100)),
                ('summery', models.CharField(max_length=500)),
                ('recivedDate', models.DateTimeField()),
                ('spradsheetLink', models.CharField(max_length=100)),
                ('relativeCommunication', models.CharField(max_length=500)),
                ('fileName', models.CharField(max_length=100)),
                ('clientId', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('response', models.CharField(max_length=400)),
                ('additionalComment', models.CharField(max_length=400)),
                ('assignTo', models.CharField(max_length=400)),
                ('assignBy', models.CharField(max_length=400)),
                ('vendorName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaireApp.AdminDB')),
            ],
        ),
    ]