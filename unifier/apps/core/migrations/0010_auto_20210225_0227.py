# Generated by Django 3.1.7 on 2021-02-25 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210223_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangachapter',
            name='images',
            field=models.JSONField(default=list, verbose_name='Images'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]