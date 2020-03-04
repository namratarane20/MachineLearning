# Generated by Django 3.0 on 2020-02-13 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0017_auto_20200213_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('response', models.TextField()),
                ('additionalComment', models.TextField()),
                ('assignTo', models.CharField(blank=True, max_length=100)),
                ('assignBy', models.CharField(blank=True, max_length=100)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questionnaireApp.AdminDB')),
            ],
        ),
    ]
