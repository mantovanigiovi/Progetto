from django.contrib import admin
from django import forms
from .models import Schnauzer, Addestramento, Prenotazione, Recensione, Notifica

# Registrazione dei modelli
admin.site.register(Schnauzer)
admin.site.register(Addestramento)
admin.site.register(Recensione)
admin.site.register(Prenotazione)

class NotificaForm(forms.ModelForm):
    class Meta:
        model = Notifica
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra le prenotazioni che non sono state annullate
        self.fields['prenotazione'].queryset = Prenotazione.objects.filter(stato='attiva')

@admin.register(Notifica)
class NotificaAdmin(admin.ModelAdmin):
    form = NotificaForm
