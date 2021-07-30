# Generated by Django 3.2.4 on 2021-07-30 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='is_mature',
            field=models.BooleanField(default=False, verbose_name='Is Mature'),
        ),
        migrations.AddField(
            model_name='novel',
            name='is_mature',
            field=models.BooleanField(default=False, verbose_name='Is Mature'),
        ),
    ]