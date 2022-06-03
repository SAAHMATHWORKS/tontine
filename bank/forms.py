from django import forms
from .models import *
from django.forms import ModelForm, TextInput, Textarea


class DateInput(forms.DateInput):
    input_type = 'date'


class BankForm(forms.ModelForm):
    class Meta:
        model = EncaissementBank
        fields = ('date', 'membre', 'operation', 'montant',)
        widgets={
                "date": DateInput(),
        }
        labels = {
            "date": "Date",
            "membre": "Membre",
            "operation": "Type d'opération",
            "montant": "Montant en FCFA",
        }

class PretBankForm(forms.ModelForm):
    class Meta:
        model = PretBank
        fields = ('date_pret', 'membre', 'profil_pret_bank', 'montant', 'avaliseur', 'date_remboursement', 'taux_interet',)
        widgets={
                "date_pret": DateInput(),
                "date_remboursement": DateInput(),
        }
        labels = {
            "date_pret": "Date du Prêt",
            "membre": "Membre",
            "profil_pret_bank": "Profil prêt",
            "montant": "Montant en FCFA",
            "avaliseur": "Avaliseur",
            "date_remboursement": "Date de Remboursement",
            "taux_interet": "Taux d'interêt en %",

        }

class PretBankiForm(forms.ModelForm):
    class Meta:
        model = PretBank
        fields = ('date_pret', 'membre', 'profil_pret_bank', 'montant', 'avaliseur', 'date_remboursement', 'taux_interet',)
        widgets={
                'montant': forms.HiddenInput(),
                'membre': forms.HiddenInput(),
                "date_pret": DateInput(),
                "date_remboursement": DateInput(),        }
        labels = {
            "date_pret": "Date du Prêt",
            "membre": "Membre",
            "profil_pret_bank": "Profil prêt",
            "montant": "Montant",
            "avaliseur": "Avaliseur",
            "date_remboursement": "Date de Remboursement",
            "taux_interet": "Taux d'interêt en %",

        }


class RemboursementPretBankForm(forms.ModelForm):
    class Meta:
        model = RemboursementPretBank
        fields = ('pretbank', 'date_remboursement', 'montant',)
        widgets={
                "date_remboursement": DateInput(),
        }
        labels = {
            "date_remboursement": "Date de Remboursement",
            "pretbank": "Id Prêt Bank",
            "montant": "Montant en FCFA",
        }