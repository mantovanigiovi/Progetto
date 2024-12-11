from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Schnauzer, Addestramento, Prenotazione, Recensione

class GeoAppTests(TestCase):
    def setUp(self):
        # Setup iniziale
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.corso = Addestramento.objects.create(
            nome="Corso Base", 
            descrizione="Descrizione corso", 
            prezzo=100
        )
        self.schnauzer = Schnauzer.objects.create(
            nome="Cucciolo", 
            taglia="nano", 
            prezzo=500, 
            descrizione="Un cucciolo adorabile"
        )
        self.data_lezione = (datetime.now() + timedelta(days=1)).date()  # Data futura per i test

    def test_home_view(self):
        # Test della vista home
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Geo/home.html')

    def test_cuccioli_nani_view(self):
        # Test della vista cuccioli nani
        response = self.client.get(reverse('cuccioli_nani'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Geo/cuccioli_nani.html')
        self.assertContains(response, self.schnauzer.nome)

    def test_login_and_prenota_view(self):
        # Test login e vista prenotazione
        self.client.login(username='testuser', password='password123')  # Simula il login
        response = self.client.get(reverse('prenota', args=[self.corso.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Geo/prenota.html')
        self.assertContains(response, self.corso.nome)

    def test_prenota_post_success(self):
        # Test prenotazione con POST
        self.client.login(username='testuser', password='password123')  # Simula il login
        response = self.client.post(
            reverse('prenota', args=[self.corso.id]),
            {
                'nome': 'Mario',
                'cognome': 'Rossi',
                'email': 'mario.rossi@example.com',
                'taglia': 'grande',
                'data': str(self.data_lezione),
                'orario': '10:00',
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect dopo la prenotazione
        self.assertTrue(Prenotazione.objects.filter(nome='Mario').exists())

    def test_prenota_post_past_date(self):
        # Test prenotazione con data nel passato
        self.client.login(username='testuser', password='password123')  # Simula il login
        response = self.client.post(
            reverse('prenota', args=[self.corso.id]),
            {
                'nome': 'Mario',
                'cognome': 'Rossi',
                'email': 'mario.rossi@example.com',
                'taglia': 'grande',
                'data': str(datetime.now().date() - timedelta(days=1)),  # Data passata
                'orario': '10:00',
            }
        )
        self.assertEqual(response.status_code, 200)  # Nessun redirect
        self.assertContains(response, "Non è possibile prenotare una lezione nel passato.")

    def test_mie_prenotazioni_view(self):
        # Test vista delle prenotazioni personali
        self.client.login(username='testuser', password='password123')  # Simula il login
        
        Prenotazione.objects.create(
            corso=self.corso,
            nome='Mario',
            cognome='Rossi',
            email='mario.rossi@example.com',
            taglia='media',
            data_lezione=self.data_lezione,
            orario_lezione='10:00',
            user=self.user
        )
        response = self.client.get(reverse('mie_prenotazioni'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Geo/mie_prenotazioni.html')
        self.assertContains(response, 'testuser')  # Verifica che il nome dell'utente (Mario) sia visibile nella pagina

    def test_recensione_post(self):
        # Test invio recensione
        self.client.login(username='testuser', password='password123')  # Simula il login
        response = self.client.post(reverse('recensione'), {'voto': 5, 'testo': 'Ottimo corso!'})
        self.assertEqual(response.status_code, 302)  # Redirect dopo il salvataggio
        self.assertTrue(Recensione.objects.filter(testo='Ottimo corso!').exists())

    def test_search_results(self):
        # Test della vista di ricerca
        response = self.client.get(reverse('search_results') + '?query=cucciolo')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Geo/search_results.html')
        self.assertContains(response, self.schnauzer.nome)
