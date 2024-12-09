from django.db import models
from django.contrib.auth.models import User

class Schnauzer(models.Model):
    TAGLIA_CHOICES = [
        ('nano', 'Cucciolo Nano'),
        ('standard', 'Cucciolo Standard'),
        ('gigante', 'Cucciolo Gigante'),
    ]

    COLORE_CHOICES = [
        ('nero', 'Nero'),
        ('sale_pepe', 'Sale e Pepe'),
        ('nero_argento', 'Nero e Argento'),
    ]

    SESSO_CHOICES = [
        ('maschio', 'Maschio'),
        ('femmina', 'Femmina'),
    ]

    nome = models.CharField(max_length=30)
    immagine = models.ImageField(upload_to='cuccioli/', blank=True, null=True)
    prezzo = models.FloatField()
    taglia = models.CharField(max_length=10, choices=TAGLIA_CHOICES)
    colore = models.CharField(max_length=15, choices=COLORE_CHOICES, blank=True, null=True)  # Aggiunto campo colore
    sesso = models.CharField(max_length=10, choices=SESSO_CHOICES, null=True, blank=True)
    descrizione = models.TextField(null=True, blank=True)
    data_di_nascita = models.DateField(default='2024-01-01')

    def __str__(self):
        return f"{self.nome} - {self.taglia}"

class Addestramento(models.Model):
    TIPO_CHOICES = [
        ('agility', 'Agility'),
        ('obedience', 'Obedience'),
    ]

    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    descrizione = models.TextField()
    immagine = models.ImageField(default='path/to/default/image.jpg')
    durata = models.PositiveIntegerField(default=60)  # Durata in minuti
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 

    def __str__(self):
        return f"{self.nome} - {self.tipo}"

class Prenotazione(models.Model):
    STATO_CHOICES = [
        ('attiva', 'Attiva'),
        ('annullata', 'Annullata'),
    ]
    
    corso = models.ForeignKey(Addestramento, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, default='Unknown')
    cognome = models.CharField(max_length=100, default='Unknown')
    email = models.EmailField(default='unknown@example.com')
    taglia = models.CharField(max_length=10, choices=[('grande', 'Grande'), ('media', 'Media'), ('piccola', 'Piccola')], default='media')
    data_lezione = models.DateField()
    orario_lezione = models.CharField(max_length=5)  # Orario in formato HH:MM
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stato = models.CharField(max_length=10, choices=STATO_CHOICES, default='attiva')

    def __str__(self):
        return f"Prenotazione per {self.nome} {self.cognome} - {self.data_lezione} {self.orario_lezione}"

class Recensione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    voto = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Voto da 1 a 5
    testo = models.TextField()
    foto = models.ImageField(upload_to='recensioni/', blank=True, null=True)  # Campo per la foto
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Recensione da {self.utente.username} - Voto: {self.voto}'

class Notifica(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)  # L'utente che riceve la notifica
    prenotazione = models.ForeignKey(Prenotazione, on_delete=models.CASCADE)  # La prenotazione che è stata annullata
    messaggio = models.CharField(max_length=500)  # Il messaggio della notifica
    data_creazione = models.DateTimeField(auto_now_add=True)  # Data e ora della creazione della notifica

    def save(self, *args, **kwargs):
        # Cambia lo stato della prenotazione a "annullata" quando viene notificata
        if self.prenotazione.stato != 'annullata':
            self.prenotazione.stato = 'annullata'
            self.prenotazione.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notifica per {self.utente} riguardo il corso {self.prenotazione.corso.nome}"
