# Generated by Django 4.2.2 on 2023-07-07 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collectibles_db_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]