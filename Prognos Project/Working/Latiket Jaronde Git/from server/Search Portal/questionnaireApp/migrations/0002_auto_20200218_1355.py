# Generated by Django 3.0 on 2020-02-18 13:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaireApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorName', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('receivedDate', models.DateTimeField(null=True)),
                ('submittedDate', models.DateTimeField(null=True)),
                ('googleSheetLink', models.CharField(max_length=200, null=True)),
                ('documentLink', models.CharField(max_length=200, null=True)),
                ('relatedCommunication', models.TextField(null=True)),
                ('fileName', models.CharField(max_length=100)),
                ('clientId', models.CharField(max_length=100)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FileUploadReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=200)),
                ('noOfRows', models.IntegerField()),
                ('uploadedBy', models.CharField(max_length=100)),
                ('updatedBy', models.CharField(max_length=100)),
                ('uploadedTime', models.DateTimeField(auto_now_add=True)),
                ('updatedTime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=100)),
                ('image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='KeywordSearchedDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=100)),
                ('keyword', models.CharField(max_length=100)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MostFavouredResponseHistoryDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=100)),
                ('vendorName', models.CharField(max_length=100)),
                ('question', models.TextField()),
                ('response', models.TextField()),
                ('additionalComment', models.TextField()),
                ('status', models.CharField(max_length=50)),
                ('time', models.DateTimeField(auto_now=True)),
                ('keyword', models.CharField(max_length=200)),
            ],
        ),
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
        migrations.CreateModel(
            name='UserSessionDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=100)),
                ('login', models.DateTimeField(auto_now_add=True)),
                ('logout', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='tagwithinfo',
            old_name='userName',
            new_name='createdBy',
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
        migrations.CreateModel(
            name='QuestionDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('response', models.TextField()),
                ('additionalComment', models.TextField()),
                ('assignTo', models.CharField(blank=True, max_length=100)),
                ('assignBy', models.CharField(blank=True, max_length=100)),
                ('exactmatch', models.IntegerField(default=0)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questionnaireApp.AdminDB')),
            ],
        ),
    ]
