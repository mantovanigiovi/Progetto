# Generated by Django 5.0.3 on 2024-03-21 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Geo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schnauzer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('immagine', models.ImageField(upload_to='')),
                ('prezzo', models.FloatField()),
                ('taglia', models.CharField(choices=[('nano', 'Cucciolo Nano'), ('standard', 'Cucciolo Standard'), ('gigante', 'Cucciolo Gigante')], max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Giganti',
        ),
        migrations.DeleteModel(
            name='Nani',
        ),
        migrations.DeleteModel(
            name='Standard',
        ),
    ]
