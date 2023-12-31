# Generated by Django 4.2.2 on 2023-11-22 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='color_theme',
            field=models.PositiveSmallIntegerField(choices=[(1, 'light'), (2, 'dark')], default=1, verbose_name='color_theme'),
        ),
        migrations.AddField(
            model_name='profile',
            name='display_style',
            field=models.PositiveSmallIntegerField(choices=[(1, 'grid'), (2, 'list')], default=1, verbose_name='display_style'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_notification',
            field=models.BooleanField(default=True, verbose_name='is_notification'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_verification',
            field=models.BooleanField(default=True, verbose_name='is_verification'),
        ),
        migrations.AddField(
            model_name='profile',
            name='paginate_by',
            field=models.PositiveSmallIntegerField(choices=[(12, '12 items per page'), (24, '24 items per page'), (36, '36 items per page'), (48, '48 items per page')], default=12, verbose_name='paginate_by'),
        ),
    ]
