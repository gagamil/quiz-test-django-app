# Generated by Django 3.1.7 on 2021-02-25 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Administrator'), (2, 'Simple user')], default=2),
        ),
    ]
