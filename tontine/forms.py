from django import forms
from .models import *
from django.forms import ModelForm, TextInput, Textarea, NumberInput

class DateInput(forms.DateInput):
    input_type = 'date'


class ConsigneForm(forms.ModelForm):
    class Meta:
        model = Consigne
        fields = ('membre', 'montant_consigne', 'date_consigne', 'penalite_consigne',)
        widgets={
                "date_consigne": DateInput(format=('%Y-%m-%d')),
        }
        labels = {
            "date_consigne": "Date Consigne",
            "membre": "Membre",
            "montant_consigne": "Montant Consigné en FCFA",
            "penalite_consigne": "Pénalité Consigne en FCFA",
        }

#Seance
class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ('date_seance', 'exercice_tontine', 'exercice_presence', 'president_jour', )
        widgets={
                #'president_jour': TextInput(attrs={'placeholder': 'Président de la séance'}),
                "date_seance": DateInput(format=('%Y-%m-%d')),
        }
        labels = {
            "date_seance": "Date Séance",
            "president_jour": "Président du Jour",
            "exercice_tontine": "Exercice Tontine",
            "exercice_presence": "Exercice Présence",
            "exercice_presence": "Exercice Présence",
        }






# Formulaire avaliseur
class AvaliseurForm(forms.ModelForm):
    class Meta:
        model = Avaliseur
        fields = ('membre',)
        labels = {
            "membre": "Membre",
        }



# Formulaire pour créer un bénéficiare
class BeneficiaireTontineForm(forms.ModelForm):
    class Meta:
        model = BeneficiaireTontine
        fields = ('seance', 'membre', 'montant', 'avaliseur', 'enchere')
        
        labels = {
            "seance": "Date Séance",
            "membre": "Membre",
            "montant": "Montant",
            "avaliseur": "Avaliseur",
            "enchere": "Valeur de l'enchère"
        }



# Formulaire pour créer un bénéficiare présence
class BeneficiairePresenceForm(forms.ModelForm):
    class Meta:
        model = BeneficiairePresence
        fields = ('seance', 'membre', 'montant', 'enchere',)
        
        labels = {
            "seance": "Date Séance",
            "membre": "Membre",
            "montant": "Montant",
            "enchere": "Valeur de l'enchère",   
        }


# Formulaire pour sortie et entrée diverses
class CompteAssociationForm(forms.ModelForm):
    class Meta:
        model = CompteAssociation
        fields = ('operation', 'date', 'motif', 'montant', 'description')
        widgets={
                "date": DateInput(format=('%Y-%m-%d')),
                'description': Textarea(attrs={'placeholder': 'Description', 'rows': 2
                }),
        }
        labels = {
            "operation": "Opération",
            "date": "Date",
            "motif": "Motif",
            "montant": "Montant en FCFA",
            "Description": "Description"
        }


# Formulaire pour sanction disciplinaire
class SanctionDisciplinaireForm(forms.ModelForm):
    class Meta:
        model = SanctionDisciplinaire
        fields = ('membre', 'date', 'motif', 'montant', 'description')
        widgets={
                "date": DateInput(format=('%Y-%m-%d')),
        }
        labels = {
            "membre": "Membre",
            "date": "Date",
            "motif": "Motif",
            "montant": "Montant en FCFA",
            "description": "Description"
        }




#libelle contribution individuele
class LibelleContributionForm(forms.ModelForm):
    class Meta:
        model = LibelleContribution
        fields = ('libelle',  'date', 'minimum')
        widgets={
                "date": DateInput(format=('%Y-%m-%d')),
        }
        labels = {
            "libelle": "Libellé",
            "date": "Date",
            "minimum": "Montant en FCFA",

        }
