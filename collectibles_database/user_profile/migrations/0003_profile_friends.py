# Generated by Django 4.2.2 on 2023-07-01 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, to='user_profile.profile'),
        ),
    ]