# Generated by Django 5.1.3 on 2024-11-22 12:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Geo', '0014_recensione'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prenotazione',
            name='taglia_cane',
        ),
        migrations.RemoveField(
            model_name='prenotazione',
            name='utente',
        ),
        migrations.AddField(
            model_name='prenotazione',
            name='cognome',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='prenotazione',
            name='email',
            field=models.EmailField(default='unknown@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='prenotazione',
            name='nome',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='prenotazione',
            name='taglia',
            field=models.CharField(choices=[('grande', 'Grande'), ('media', 'Media'), ('piccola', 'Piccola')], default='media', max_length=10),
        ),
        migrations.AddField(
            model_name='prenotazione',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prenotazione',
            name='corso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Geo.addestramento'),
        ),
        migrations.AlterField(
            model_name='prenotazione',
            name='orario_lezione',
            field=models.CharField(max_length=5),
        ),
    ]
