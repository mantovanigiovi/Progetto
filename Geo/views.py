from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from .models import Schnauzer
from .models import Addestramento
from .models import Prenotazione, Notifica
from .models import Recensione
from .forms import CreateUserForm
from django.db.models import Q  # Importa Q per query complesse

from django.contrib import messages

def home(request):
    return render(request, 'Geo/home.html', {})

def navbar(request):
    return render(request, 'Geo/navbar.html')

def cuccioli_nani(request):
    cuccioli = Schnauzer.objects.filter(taglia='nano')
    order_by = request.GET.get('order_by', 'prezzo')
    direction = request.GET.get('direction', 'asc')

    if direction == 'asc':
        cuccioli = cuccioli.order_by(order_by)
    else:
        cuccioli = cuccioli.order_by(f'-{order_by}')

    return render(request, 'Geo/cuccioli_nani.html', {'cuccioli_nani': cuccioli})   

def cuccioli_standard(request):
    cuccioli = Schnauzer.objects.filter(taglia='standard')
    order_by = request.GET.get('order_by', 'prezzo')
    direction = request.GET.get('direction', 'asc')

    if direction == 'asc':
        cuccioli = cuccioli.order_by(order_by)
    else:
        cuccioli = cuccioli.order_by(f'-{order_by}')

    return render(request, 'Geo/cuccioli_standard.html', {'cuccioli_standard': cuccioli})

def cuccioli_gigante(request):
    cuccioli = Schnauzer.objects.filter(taglia='gigante')
    order_by = request.GET.get('order_by', 'prezzo')
    direction = request.GET.get('direction', 'asc')

    if direction == 'asc':
        cuccioli = cuccioli.order_by(order_by)
    else:
        cuccioli = cuccioli.order_by(f'-{order_by}')

    return render(request, 'Geo/cuccioli_gigante.html', {'cuccioli_gigante': cuccioli})

def contatti(request):
    return render(request, 'Geo/contatti.html')

def razza(request):
    return render(request, 'Geo/razza.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account creato correttamente per ' + user)

            return redirect('login')

    return render (request, 'Geo/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username o Password non corretti')

    return render(request, 'Geo/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def search_results(request):
    query = request.GET.get('query', '').strip()  # Recupera e pulisce la query
    if query:  # Se la query non è vuota, filtra i risultati
        results = Schnauzer.objects.filter(
            Q(nome__icontains=query) | Q(descrizione__icontains=query)
        )
    else:
        results = Schnauzer.objects.none()  # Mostra tutti i risultati se la query è vuota

    return render(request, 'Geo/search_results.html', {'results': results, 'query': query})


def dettaglio_cucciolo(request, cucciolo_id):
    cucciolo = get_object_or_404(Schnauzer, pk=cucciolo_id)
    return render(request, 'Geo/dettaglio_cucciolo.html', {'cucciolo': cucciolo})

@login_required
def prenota(request, corso_id):
    corso = get_object_or_404(Addestramento, id=corso_id)
    corsi = Addestramento.objects.all()

    # Lista degli orari disponibili di default
    orari_disponibili = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00","19:00"]
    orari_prenotati = []

    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        taglia = request.POST.get('taglia')
        data_lezione = request.POST.get('data')
        orario_lezione = request.POST.get('orario')

        data_lezione = datetime.strptime(data_lezione, '%Y-%m-%d').date()
        if data_lezione < timezone.now().date():
            messages.error(request, "Non è possibile prenotare una lezione nel passato.")
            return render(request, 'Geo/prenota.html', {
                'corso': corso,
                'corsi': corsi,
                'corso_id': corso.id,
                'orari_disponibili': orari_disponibili,
                'nome': nome,
                'cognome': cognome,
                'email': email,
                'taglia': taglia,
                'data_lezione': data_lezione,  # Passiamo i dati immessi
                'orario_lezione': orario_lezione,
            })

        orari_prenotati = list(Prenotazione.objects.filter(corso=corso, data_lezione=data_lezione).values_list('orario_lezione', flat=True))

        if orario_lezione in orari_prenotati:
            messages.error(request, f"Orario {orario_lezione} già prenotato per questa data.")
        else:
            prenotazione = Prenotazione(
                corso=corso,
                nome=nome,
                cognome=cognome,
                email=email,
                taglia=taglia,
                data_lezione=data_lezione,
                orario_lezione=orario_lezione,
                user=request.user
            )
            prenotazione.save()
            messages.success(request, f"Prenotazione effettuata per il {data_lezione} alle {orario_lezione}.")
            return redirect('mie_prenotazioni')

    # Verifica se la richiesta è AJAX usando l'intestazione X-Requested-With
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        data_selezionata = request.GET.get('data')
        orari_prenotati = list(Prenotazione.objects.filter(corso=corso, data_lezione=data_selezionata).values_list('orario_lezione', flat=True))
        orari_non_prenotati = [orario for orario in orari_disponibili if orario not in orari_prenotati]

        return JsonResponse({'orari': orari_non_prenotati})

    return render(request, 'Geo/prenota.html', {
        'corso': corso,
        'corsi': corsi,
        'corso_id': corso.id,
        'orari_disponibili': orari_disponibili,
    })

def addestramento(request):
    corsi_addestramento = Addestramento.objects.all()
    return render(request, 'Geo/addestramento.html', {'corsi_addestramento': corsi_addestramento})

def dettaglio_corso(request, corso_id):
    corso = get_object_or_404(Addestramento, id=corso_id)
    return render(request, 'Geo/dettaglio_corso.html', {'corso': corso})

@login_required
def mie_prenotazioni(request):
    ordine = request.GET.get('ordine', 'asc')  # Recupera il parametro di ordinamento
    solo_attive = request.GET.get('solo_attive', 'off') == 'on'  # Controlla se il checkbox è selezionato
    
    # Filtra le prenotazioni in base al checkbox
    if solo_attive:
        prenotazioni = Prenotazione.objects.filter(user=request.user, stato='attiva')
    else:
        prenotazioni = Prenotazione.objects.filter(user=request.user)

    # Applica ordinamenti
    if ordine == 'asc':
        prenotazioni = prenotazioni.order_by('data_lezione')
    elif ordine == 'desc':
        prenotazioni = prenotazioni.order_by('-data_lezione')
    elif ordine == 'prezzo_asc':
        prenotazioni = prenotazioni.order_by('corso__prezzo')
    elif ordine == 'prezzo_desc':
        prenotazioni = prenotazioni.order_by('-corso__prezzo')

    return render(request, 'Geo/mie_prenotazioni.html', {
        'prenotazioni': prenotazioni,
        'ordine': ordine,
        'solo_attive': solo_attive,  # Per mantenere il valore del checkbox nel template
    })


@login_required(login_url='/not-logged-in/')
def recensione(request):
    if request.method == 'POST':
        voto = request.POST.get('voto')
        testo = request.POST.get('testo')
        foto = request.FILES.get('foto')

        try:
            Recensione.objects.create(
                utente=request.user,
                voto=voto,
                testo=testo,
                foto=foto
            )
            messages.success(request, 'Recensione inviata con successo!')
            return redirect('recensione')  # Ricarica la pagina per mostrare la nuova recensione
        except Exception as e:
            messages.error(request, f'Errore nell\'invio della recensione: {str(e)}')

    # Recupera tutte le recensioni per visualizzarle sotto il form
    recensioni = Recensione.objects.all().order_by('-id')  # Ordinamento discendente per le recensioni più recenti

    return render(request, 'Geo/recensione.html', {'recensioni': recensioni})

@login_required
def annulla_prenotazione(prenotazione_id):
    prenotazione = Prenotazione.objects.get(id=prenotazione_id)
    prenotazione.stato = 'annullata'
    prenotazione.save()

    # Creare una notifica per l'utente
    messaggio = f"La tua prenotazione per {prenotazione.corso.nome} è stata annullata."
    notifica = Notifica.objects.create(
        utente=prenotazione.user,
        prenotazione=prenotazione,
        messaggio=messaggio
    )
    notifica.save()


@login_required
def elimina_prenotazione(request, prenotazione_id):
    prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id)
    prenotazione.delete()
    messages.success(request, "Prenotazione eliminata con successo.")
    return redirect('mie_prenotazioni')

# Vista dedicata per la pagina "Non loggato"
def not_logged_in(request):
    return render(request, 'Geo/not_logged_in.html')
