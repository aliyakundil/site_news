# Generated by Django 4.1.7 on 2023-03-22 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_remove_post_tag_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='video',
            name='likedone',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.DeleteModel(
            name='LikeDislike',
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
