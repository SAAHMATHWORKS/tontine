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
        fields = ('date_pret', 'membre', 'profil_pret_bank', 'montant', 'garantie', 'date_remboursement', 'taux_interet',)
        widgets={
                "date_pret": DateInput(),
                "date_remboursement": DateInput(),
        }
        labels = {
            "date_pret": "Date du Prêt",
            "membre": "Membre",
            "profil_pret_bank": "Profil prêt",
            "montant": "Montant en FCFA",
            "garantie": "Garantie",
            "date_remboursement": "Date de Remboursement",
            "taux_interet": "Taux d'interêt en %",

        }

class PretBankiForm(forms.ModelForm):
    class Meta:
        model = PretBank
        fields = ('date_pret', 'montant', 'profil_pret_bank', 'date_remboursement', 'taux_interet', 'garantie','membre',)
        widgets={
                'montant': TextInput(attrs={'readonly': 'readonly'} ),
                'membre': forms.HiddenInput(),
                "date_pret": DateInput(),
                "date_remboursement": DateInput(), }
        labels = {
            "date_pret": "Date du Prêt",
            "montant": "Montant",
            "profil_pret_bank": "Profil prêt",         
            "date_remboursement": "Date de Remboursement",
            "taux_interet": "Taux d'interêt en %",
            "avaliseur": "Avaliseur",
            "membre": "Membre",

        }


class RemboursementPretBankForm(forms.ModelForm):
    class Meta:
        model = RemboursementPretBank
        fields = ('pretbank', 'date_remboursement', 'montant',)
        widgets={
                "date_remboursement": DateInput(),
                "pretbank": TextInput(attrs={'readonly': 'readonly'} ),
        }
        labels = {
            "date_remboursement": "Date de Remboursement",
            "pretbank": "Id Prêt Bank",
            "montant": "Montant en FCFA",
        }