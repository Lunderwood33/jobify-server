# Generated by Django 3.2.10 on 2021-12-10 17:07

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
            name='JobifyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('bio', models.CharField(max_length=50)),
                ('isBusiness', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55)),
                ('description', models.TextField()),
                ('wage', models.IntegerField()),
                ('url', models.CharField(max_length=150)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobifyapi.jobifyuser')),
            ],
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='JobListingUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobifyapi.joblisting')),
                ('jobify_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobifyapi.jobifyuser')),
            ],
        ),
        migrations.AddField(
            model_name='joblisting',
            name='interested',
            field=models.ManyToManyField(related_name='interested', through='jobifyapi.JobListingUser', to='jobifyapi.JobifyUser'),
        ),
        migrations.AddField(
            model_name='joblisting',
            name='job_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobifyapi.jobtype'),
        ),
    ]
