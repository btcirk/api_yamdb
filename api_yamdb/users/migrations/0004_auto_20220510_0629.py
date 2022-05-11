# Generated by Django 2.2.16 on 2022-05-10 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220510_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('a', 'admin'), ('m', 'moderator'), ('u', 'user')], default='u', max_length=1, verbose_name='Роль пользователя'),
        ),
    ]
