# Generated by Django 5.0.3 on 2024-03-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Geo', '0005_schnauzer_colore'),
    ]

    operations = [
        migrations.AddField(
            model_name='schnauzer',
            name='data_di_nascita',
            field=models.DateField(default='2024-01-01'),
        ),
    ]
