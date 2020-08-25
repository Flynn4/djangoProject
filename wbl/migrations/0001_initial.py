# Generated by Django 3.0.3 on 2020-08-25 07:23

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
            name='Criterion',
            fields=[
                ('criterionId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('detail', models.TextField(default=' ')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalMark', models.IntegerField(default=0)),
                ('averageMark', models.FloatField(default=0)),
                ('finalComment', models.TextField(default=' ')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('roleId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('role_have', models.ManyToManyField(blank=True, to='wbl.Criterion')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isStudent', models.BooleanField(default=False)),
                ('isMentor', models.BooleanField(default=False)),
                ('isStaff', models.BooleanField(default=False)),
                ('test', models.TextField(default='  ')),
                ('role', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wbl.Role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('detail', models.TextField(default=' ')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('limit_time', models.DateTimeField()),
                ('progress', models.IntegerField(default=0)),
                ('include_criterion', models.ManyToManyField(blank=True, to='wbl.Criterion')),
            ],
        ),
        migrations.CreateModel(
            name='PeerReviewMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=0)),
                ('criterion', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wbl.Criterion')),
                ('evaluation', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wbl.Evaluation')),
                ('rater', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'peer_review_mark',
            },
        ),
        migrations.AddField(
            model_name='evaluation',
            name='peer_review_mark',
            field=models.ManyToManyField(blank=True, through='wbl.PeerReviewMark', to='wbl.Criterion'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='rater',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='task',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wbl.Task'),
        ),
    ]
