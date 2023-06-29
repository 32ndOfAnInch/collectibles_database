# Generated by Django 4.2.2 on 2023-06-29 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collectibles_db_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradingsystem',
            name='condition',
        ),
        migrations.AlterField(
            model_name='collectibleitem',
            name='condition',
            field=models.CharField(max_length=50, verbose_name='condition'),
        ),
        migrations.DeleteModel(
            name='Condition',
        ),
        migrations.DeleteModel(
            name='GradingSystem',
        ),
    ]
