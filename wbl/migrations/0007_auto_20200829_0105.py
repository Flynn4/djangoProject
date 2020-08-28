# Generated by Django 3.0.3 on 2020-08-28 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wbl', '0006_auto_20200828_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='peer_review_mark',
            field=models.ManyToManyField(blank=True, related_name='peer_review_mark_1', through='wbl.PeerReviewMark', to='wbl.Criterion'),
        ),
    ]
