# Generated by Django 5.1.3 on 2024-11-28 11:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Geo', '0023_notifica_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifica',
            name='prenotazione',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Geo.prenotazione'),
        ),
        migrations.AlterField(
            model_name='notifica',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prenotazione',
            name='cognome',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='prenotazione',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='prenotazione',
            name='nome',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='prenotazione',
            name='taglia',
            field=models.CharField(max_length=10),
        ),
    ]
