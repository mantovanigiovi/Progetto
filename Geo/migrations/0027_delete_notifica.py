# Generated by Django 5.1.3 on 2024-11-28 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Geo', '0026_remove_notifica_user_alter_prenotazione_cognome_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notifica',
        ),
    ]