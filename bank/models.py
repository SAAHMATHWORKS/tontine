from django.db import models
from tontine.models import Membre
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

OP_TYPES = (
    ('DEPÔT', 'DEPÔT'),
    ('RETRAIT', 'RETRAIT'),
    ('INTERÊT', 'INTERÊT'),
)
#Encaissement banque
class EncaissementBank(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date = models.DateTimeField()
    operation = models.CharField(choices=OP_TYPES, max_length=7)
    montant = models.PositiveIntegerField()
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    @property
    def value(self):
        if self.operation == 'RETRAIT':
            return -self.montant
        return self.montant



# type de prêt
class ProfilPretBank(models.Model):
    profil_pret = models.CharField(max_length=100, unique=True)
    montant_min = models.PositiveIntegerField()
    montant_max = models.PositiveIntegerField()
    def __str__(self):
        return f'{self.profil_pret}  {self.montant_min} - {self.montant_max}'

# Prêt à la banque
class PretBank(models.Model):
    date_pret =models.DateTimeField()
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    profil_pret_bank = models.ForeignKey(ProfilPretBank, on_delete=models.SET_NULL, blank=True, null=True)
    montant = models.PositiveIntegerField()
    avaliseur = models.CharField(max_length=50, blank=True, null=True)
    date_remboursement =models.DateTimeField()
    taux_interet = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    versement_remboursement = models.PositiveIntegerField(default=0)
    freeze = models.BooleanField(default=False)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.membre.nom}-{self.montant}-{self.date_pret} '
    
    @property
    def montant_initial_remboursement(self):
        m = int(self.montant*(1+self.taux_interet*0.01))
        return m

    @property
    def reste_a_rembourser(self):
        v = self.montant_initial_remboursement - self.versement_remboursement
        return v
    
    @property
    def insolvable(self):
        now = timezone.now()
        if self.reste_a_rembourser >0 and now > self.date_remboursement:
            return True
        else:
            return False




# Remboursement prêt bancaire reste_a_rembourser montant_remboursement
class RemboursementPretBank(models.Model):
    pretbank = models.ForeignKey(PretBank, on_delete=models.CASCADE)
    date_remboursement =models.DateTimeField()
    montant = models.PositiveIntegerField()
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)







