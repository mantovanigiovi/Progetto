# Generated by Django 5.1.3 on 2024-11-28 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Geo', '0021_notifica_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifica',
            name='user',
        ),
    ]
