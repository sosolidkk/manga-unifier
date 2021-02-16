# Generated by Django 3.1.6 on 2021-02-16 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210216_1318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelOptions(
            name='manga',
            options={'verbose_name': 'Manga', 'verbose_name_plural': 'Mangas'},
        ),
        migrations.AlterModelOptions(
            name='mangachapter',
            options={'verbose_name': 'Manga Chapter', 'verbose_name_plural': 'Manga Chapters'},
        ),
        migrations.AlterModelOptions(
            name='novel',
            options={'verbose_name': 'Novel', 'verbose_name_plural': 'Novels'},
        ),
        migrations.AlterModelOptions(
            name='novelchapter',
            options={'verbose_name': 'Novel Chapter', 'verbose_name_plural': 'Novel Chapters'},
        ),
        migrations.AlterModelOptions(
            name='platform',
            options={'verbose_name': 'Platform', 'verbose_name_plural': 'Platforms'},
        ),
    ]
