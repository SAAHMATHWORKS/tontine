from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(MontantBank)
admin.site.register(MontantAgape)
admin.site.register(MontantPresence)
admin.site.register(MontantCotisation)
admin.site.register(Seance)
admin.site.register(Sanction) 




@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ['nom','matricule','date_adhesion','telephone',]
    list_filter = ['sexe', 'cotisation', 'bank_bool', 'cotisation_bool']
    search_fields = ['nom']


@admin.register(Encaissement)
class EncaissementAdmin(admin.ModelAdmin):
    list_display = ['seance', 'membre', 'reglement', 'tontine_cotisation', 'updated', 'author']
    list_filter = ['seance', 'tontine_cotisation', 'echec_cotisation', 'echec_presence', 'echec_agape']
    search_fields = ['membre__nom',]


#Avaliseur
@admin.register(Avaliseur)
class AvaliseurAdmin(admin.ModelAdmin):
    list_display = ['membre', 'author']
    search_fields = ['membre',]


@admin.register(BeneficiaireTontine)
class BeneficiaireTontineAdmin(admin.ModelAdmin):
    list_display = ['seance', 'membre', 'montant', 'avaliseur', 'enchere','author']
    list_filter = ['seance',]
    search_fields = ['membre', 'avaliseur']


@admin.register(BeneficiairePresence)
class BeneficiairePresenceAdmin(admin.ModelAdmin):
    list_display = ['seance', 'membre', 'montant', 'enchere','author']
    list_filter = ['seance',]
    search_fields = ['membre__nom',]





@admin.register(Consigne)
class ConsigneAdmin(admin.ModelAdmin):
    list_display = ['membre', 'montant_consigne', 'date_consigne', 'updated', 'created', 'author']
    search_fields = ['membre__nom',]






@admin.register(CompteAssociation)
class CompteAssociationAdmin(admin.ModelAdmin):
    list_display = ['operation', 'montant', 'date', 'motif', 'updated', 'created', 'author']
    search_fields = ['operation',]


@admin.register(SanctionDisciplinaire)
class SanctionDisciplinaireAdmin(admin.ModelAdmin):
    list_display = ['membre', 'montant', 'date', 'motif', 'updated', 'created', 'author']
    search_fields = ['membre__nom',]




@admin.register(LibelleContribution)
class LibelleContributionAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'date',]



@admin.register(ContributionIndividuelle)
class ContributionIndividuelleAdmin(admin.ModelAdmin):
    list_display = ['motif','membre', 'reglement',]
    search_fields = ['membre__nom',]


@admin.register(VersementContributionIndividuelle)
class VersementContributionIndividuelleAdmin(admin.ModelAdmin):
    list_display = ['contrib_ind', 'montant',]


@admin.register(ExerciceTontine)
class ExerciceTontineAdmin(admin.ModelAdmin):
    list_display = ['date_debut','is_active', 'created', 'updated', 'author']
    search_fields = ['author',]



@admin.register(ExercicePresence)
class ExercicePresenceAdmin(admin.ModelAdmin):
    list_display = ['date_debut','is_active', 'created', 'updated', 'author']
    search_fields = ['author',]