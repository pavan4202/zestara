# Generated by Django 3.2.7 on 2022-06-16 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_video_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='user',
            new_name='channel_name',
        ),
    ]
