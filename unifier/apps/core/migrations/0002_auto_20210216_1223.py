# Generated by Django 3.1.6 on 2021-02-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Novel rate'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='novel',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Novel rate'),
        ),
    ]
