from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


SEXE_CHOICES = (
    ('M', 'M'),
    ('F', 'F'),
)

TYPE_OPERATION = (
    ('ENTREE', 'ENTREE'),
    ('SORTIE', 'SORTIE'),
)




# Montant présence
class MontantPresence(models.Model):
    montant = models.PositiveIntegerField(unique=True)
    sanction = models.PositiveIntegerField(unique=True, default=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.montant)


# Montant sport
class MontantSport(models.Model):
    montant = models.PositiveIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.montant)
   

class MontantCotisation(models.Model):
    montant = models.PositiveIntegerField(unique=True)
    taux_sanction_before = models.PositiveIntegerField(default=30)
    taux_sanction_after = models.PositiveIntegerField(default=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.montant)

class MontantBank(models.Model):
    montant = models.PositiveIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.montant)


class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100, unique=True)
    matricule = models.CharField(max_length=8, unique=True)
    telephone = models.CharField(max_length=10, blank=True, null=True)
    qualite = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    sexe = models.CharField(choices=SEXE_CHOICES, max_length=1)
    date_naissance = models.DateField(blank=True, null=True)
    date_adhesion = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cotisation = models.ForeignKey(MontantCotisation, on_delete=models.CASCADE)
    presence = models.ForeignKey(MontantPresence, on_delete=models.CASCADE)
    sport = models.ForeignKey(MontantSport, on_delete=models.CASCADE)
    bank = models.ForeignKey(MontantBank, on_delete=models.SET_NULL, blank=True, null=True)
    bank_bool = models.BooleanField(default=False)
    cotisation_bool = models.BooleanField(default=False)
    presence_bool = models.BooleanField(default=True)
    total_impaye = models.IntegerField(default=0)
    total_seance = models.IntegerField(default=0)
    total_consigne = models.IntegerField(default=0)
    reserve = models.IntegerField(default=0)


    def __str__(self):
        return self.nom

# Exercice Tontine
class ExerciceTontine(models.Model):
    date_debut = models.DateTimeField(unique=True)
    franchise = models.PositiveIntegerField(default=0)
    date_franchise = models.DateField(unique=True)
    nbre_semaines = models.PositiveIntegerField(default=52)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.date_debut.strftime('%a %d/%m/%Y %H:%M')

# Exercice Présence
class ExercicePresence(models.Model):
    date_debut = models.DateTimeField()
    nbre_semaines = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.date_debut.strftime('%a %d/%m/%Y %H:%M')


class Seance(models.Model):
    date_seance = models.DateField(unique=True)
    president_jour = models.ForeignKey(Membre, on_delete=models.SET_NULL, blank=True, null=True)
    exercice_tontine = models.ForeignKey(ExerciceTontine, on_delete=models.CASCADE)
    exercice_presence = models.ForeignKey(ExercicePresence, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
    total_presence = models.IntegerField(default=0)
    total_sport = models.IntegerField(default=0)
    total_tontine = models.IntegerField(default=0)
    total_encais = models.IntegerField(default=0)
    nbechec_sport= models.IntegerField(default=0)
    nbechec_presence= models.IntegerField(default=0)
    nbechec_cotisation= models.IntegerField(default=0)
    mtechec_sport= models.IntegerField(default=0)
    mtechec_presence= models.IntegerField(default=0)
    mtechec_cotisation= models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return str(self.date_seance)

    @property
    def tontine_is_active(self):
        if self.exercice_tontine.is_active:
            return True
        return False

    @property
    def presence_is_active(self):
        if self.exercice_presence.is_active:
            return True
        return False

class Encaissement(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    reglement = models.PositiveIntegerField(default=0)
    tontine_presence = models.PositiveIntegerField(default=0)
    tontine_sport = models.PositiveIntegerField(default=0)
    tontine_cotisation = models.PositiveIntegerField(default=0)
    echec_presence = models.BooleanField(default=False)
    echec_sport = models.BooleanField(default=False)
    echec_cotisation = models.BooleanField(default=False)
    called = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def tontine_is_active(self):
        if self.seance.tontine_is_active:
            return True
        return False

    @property
    def presence_is_active(self):
        if self.seance.presence_is_active:
            return True
        return False


    @property
    def montant_attendu(self):
        p=self.membre.presence.montant
        sp =self.membre.sport.montant
        c=self.membre.cotisation.montant
        attendu = int(p)+int(sp)+int(c)
        return attendu
    
    @property
    def sanction_presence(self):
        sanction_presence = self.membre.presence.sanction
        if self.echec_presence:
            return sanction_presence
        return 0

    @property
    def sanction_sport(self):
        if self.echec_sport:
            return 0
        return 0

    @property
    def sanction_tontine(self):
        if self.echec_cotisation:
            taux_sanction_after = self.membre.cotisation.taux_sanction_after/100
            taux_sanction_before = self.membre.cotisation.taux_sanction_before/100
            #sum_beneficie = sum([s.montant for s in BeneficiaireTontine.objects.filter(membre=self.membre) if s.seance.tontine_is_active==True])
            if self.membre.cotisation.montant>0:      
                #fraction_beneficie = sum_beneficie/(self.membre.cotisation.montant * nbre_sem)
                penalite= self.membre.cotisation.montant * taux_sanction_before
                return penalite
        return 0


# Tables des consignes
class Consigne(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    montant_consigne = models.PositiveBigIntegerField()
    date_consigne = models.DateField()
    penalite_consigne = models.PositiveBigIntegerField()
    reglement = models.PositiveBigIntegerField(default=0)
    date_paiement = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    

    @property
    def consigne_paye(self):
        if self.reglement >= self.penalite_consigne:
            return 1
        return 0

# Sanction tontine
class Sanction(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    regl_sanc_tontine = models.PositiveIntegerField(default=0)
    regl_sanc_presence = models.PositiveIntegerField(default=0)
    date_paiement_sp = models.DateTimeField(blank=True, null=True)
    date_paiement_sc = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    valeur_sanction_tontine = models.PositiveIntegerField(default=0)
    valeur_sanction_presence = models.PositiveIntegerField(default=0)

    @property
    def is_active(self):
        if self.seance.tontine_is_active:
            return True
        return False


    @property
    def sanction_tontine_paye(self):
        if self.regl_sanc_tontine >= self.valeur_sanction_tontine:
            return 1
        return 0
    # timezone.now()
    @property
    def sanction_presence_paye(self):
        if self.regl_sanc_presence >= self.valeur_sanction_presence:
            return 1
        return 0
    


class Avaliseur(models.Model):
    membre = models.OneToOneField(Membre, on_delete=models.CASCADE)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.membre.nom        

    

class BeneficiaireTontine(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    montant = models.PositiveIntegerField()
    avaliseur = models.ForeignKey(Avaliseur, on_delete=models.CASCADE)
    enchere = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def is_active(self):
        if self.seance.tontine_is_active:
            return True
        return False

    @property
    def charge(self):
        list_beneficier = BeneficiaireTontine.objects.filter(membre=self.membre)
        cap_beneficier = sum([value.montant for value in list_beneficier if value.seance.tontine_is_active==True])
        d = self.membre.cotisation.montant + self.membre.presence.montant + self.membre.sport.montant
        impaye_cotisation = self.membre.total_impaye * (self.membre.cotisation.montant/d)
        impaye_cotisation = int(impaye_cotisation)
        reserve = self.membre.reserve * (self.membre.cotisation.montant/d)
        reserve = int(reserve)
        list_encais = Encaissement.objects.filter(membre=self.membre)
        entrees_cotisation = sum([c.tontine_cotisation for c in list_encais if c.tontine_is_active==True])
        cap_risque = reserve + entrees_cotisation -(impaye_cotisation+cap_beneficier)
        return -min(cap_risque, 0)
        





# Bénéficiaire présence
class BeneficiairePresence(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    montant = models.PositiveIntegerField()
    enchere = models.PositiveIntegerField(default=0)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def is_active(self):
        if self.seance.presence_is_active:
            return True
        return False




#
class CompteAssociation(models.Model):
    operation = models.CharField(choices=TYPE_OPERATION, max_length=7)
    date = models.DateTimeField()
    motif = models.CharField(max_length=255)
    montant = models.PositiveBigIntegerField()
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)



# Sanction disciplinaire
class SanctionDisciplinaire(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date = models.DateTimeField()
    motif = models.CharField(max_length=255)
    montant = models.PositiveBigIntegerField()
    reglement = models.PositiveBigIntegerField(default=0)
    description = models.TextField(blank=True)
    date_paiement = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def sanction_paye(self):
        if self.reglement >= self.montant:
            return 1
        return 0


class LibelleContribution(models.Model):
    libelle = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField()
    minimum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.libelle


class ContributionIndividuelle(models.Model):
    motif = models.ForeignKey(LibelleContribution, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    reglement = models.PositiveIntegerField(default=0)
    date_reglement = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def taux_paye(self):
        if self.reglement >= self.motif.minimum:
            return 1
        return 0

