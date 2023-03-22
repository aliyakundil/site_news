# Generated by Django 4.1.7 on 2023-03-22 09:19

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Tag')),
                ('slug', models.SlugField(default=builtins.id, unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(related_name='tags', to='main.tag'),
        ),
    ]
