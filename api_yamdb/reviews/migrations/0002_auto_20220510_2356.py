# Generated by Django 2.2.16 on 2022-05-10 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.IntegerField(blank=True),
        ),
    ]
