# Generated by Django 5.0.3 on 2024-03-22 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Geo', '0004_schnauzer_descrizione'),
    ]

    operations = [
        migrations.AddField(
            model_name='schnauzer',
            name='colore',
            field=models.CharField(blank=True, choices=[('nero', 'Nero'), ('sale_pepe', 'Sale e Pepe'), ('nero_argento', 'Nero e Argento')], max_length=15, null=True),
        ),
    ]
