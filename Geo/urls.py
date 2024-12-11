from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home, contatti, razza, register, addestramento, cuccioli_gigante, cuccioli_standard, cuccioli_nani, search_results, navbar, prenota, recensione, mie_prenotazioni, annulla_prenotazione, elimina_prenotazione

urlpatterns = [
    path('', views.home, name='home'),
    path('cuccioli_nani/', cuccioli_nani, name='cuccioli_nani'),
    path('cuccioli_standard/', cuccioli_standard, name='cuccioli_standard'),
    path('cuccioli_gigante/', cuccioli_gigante, name='cuccioli_gigante'),
    path('contatti/', contatti, name='contatti'),
    path('razza/', razza, name='razza'),
    path('register/', register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('addestramento/', addestramento, name='addestramento'),
    path('search/', search_results, name='search_results'),
    path('cucciolo/<int:cucciolo_id>/', views.dettaglio_cucciolo, name='dettaglio_cucciolo'),
    path('corso/<int:corso_id>/', views.dettaglio_corso, name='dettaglio_corso'),
    path('navbar/', navbar, name='navbar'),
    path('prenota/<int:corso_id>/', views.prenota, name='prenota'),
    path('recensione/', views.recensione, name='recensione'),
    path('annulla-prenotazione/<int:prenotazione_id>/', views.annulla_prenotazione, name='annulla_prenotazione'),
    path('elimina-prenotazione/<int:prenotazione_id>/', views.elimina_prenotazione, name='elimina_prenotazione'),
    path('mie_prenotazioni/', views.mie_prenotazioni, name='mie_prenotazioni'),
    path('not-logged-in/', views.not_logged_in, name='not_logged_in'),
]
