from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(EncaissementBank)
class EncaissementBankAdmin(admin.ModelAdmin):
    list_display = ['membre', 'date', 'operation', 'value','author']
    list_filter = ['operation',]
    search_fields = ['membre', 'operation']



@admin.register(PretBank)
class PretBankAdmin(admin.ModelAdmin):
    list_display = ['date_pret', 'montant', 'membre', 'avaliseur', 'date_remboursement','author']
    search_fields = ['membre', 'avaliseur']



@admin.register(ProfilPretBank)
class ProfilPretBankAdmin(admin.ModelAdmin):
    list_display = ['profil_pret', 'montant_min', 'montant_min',]
    search_fields = ['profil_pret']


@admin.register(RemboursementPretBank)
class RemboursementPretBankAdmin(admin.ModelAdmin):
    list_display = ['pretbank', 'date_remboursement', 'montant','author']