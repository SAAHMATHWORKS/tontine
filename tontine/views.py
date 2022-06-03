from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db.models import Sum
from .forms import *
from django.contrib import messages
from bank.models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# bank
from bank.models import *

# Create your views here.

def home(request):
	context = {}
	return render(request, 'tontine/home.html', context)



def about(request):
	context = {}
	return render(request, 'tontine/about.html', context)




@staff_member_required
def create_session(request):
    context = {}
    if request.method == "POST":
        form = SeanceForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data['date_seance']
            form.instance.author = request.user
            form.save()
            messages.info(request, f'Séance du  {d} correctement créée par {request.user}!!!')
            return redirect('post_create_session')
    else:
        form = SeanceForm()

    context['form'] = form
    return render(request, 'tontine/seance.html', context)       


@staff_member_required
def	post_create_session(request):
	if Seance.objects.all().exists():	
		for s in Seance.objects.all():
			if s.tontine_is_active:
				date_debut_exercice = s.exercice_tontine.date_debut
				if not Encaissement.objects.filter(seance=s).exists():
					# Mettre à jour les cotisations des membres
					for m in Membre.objects.filter(presence_bool=True):
						em = [obj for obj in Encaissement.objects.filter(membre=m) if obj.tontine_is_active]
						len_presence = len([obj for obj in Encaissement.objects.filter(membre=m) if obj.presence_is_active])
						# sum montant consigne du membre
						cs = Consigne.objects.filter(membre=m, date_consigne__gte = date_debut_exercice)
						sumconsigne = sum([c.montant_consigne for c in cs])
						# end sum montant consigne du membre
						#print('longueur Table encaissement:', len(em))
						attendu_tontine = len(em)* m.cotisation.montant
						attendu_presence_sport = len_presence * (m.presence.montant + m.sport.montant)
						attendu = attendu_tontine + attendu_presence_sport
						consigne = m.total_consigne
						reserve = m.reserve
						liste = [e.reglement for e in em]
						regls = sum([h for h in liste])
						calcul = attendu - regls - sumconsigne
						m.total_impaye = max(0, calcul)
						m.reserve = -min(0, calcul)
						m.total_consigne -= consigne
						m.save()
						row = Encaissement(seance = s,
						membre = m,
						reglement = 0
						)
						row.save()
		
	
	listseance = [obj for obj in Seance.objects.all().order_by("-created") if obj.tontine_is_active]

	context= {'listseance': listseance}
	return render(request, 'tontine/post_create_session.html', context)

# Page tontine avec la table des données
@staff_member_required
def tontine(request, id):
	s = get_object_or_404(Seance, pk=id)
	
	encais = Encaissement.objects.filter(seance=s).order_by('-membre__cotisation__montant')
	
	total_encaissement = sum([x.reglement for x in encais])
	total_presence = sum([x.tontine_presence for x in encais])
	total_sport =  sum([x.tontine_sport for x in encais])
	total_cotisation = sum([x.tontine_cotisation for x in encais])
	
	context = {'encais':encais,  's': s, 
	'total_encaissement': total_encaissement, 'total_presence': total_presence,
	'total_sport': total_sport, 'total_cotisation': total_cotisation} #seances': seances,
	return render(request, 'tontine/tontine.html', context)


@staff_member_required
def savedata(request):
	# mId id of target row
	mId=request.POST.get('mId')
	r=request.POST.get('r'+mId)
	reserve = request.POST.get('reserve'+mId)
	regl = int(r)
	# Get row as object of Encaissement class
	enc = get_object_or_404(Encaissement, pk=mId)
	# Get the meeting or seance
	sea = enc.seance
	# Get the member
	membre = enc.membre
	enc.reglement = regl
	p=membre.presence.montant
	s=membre.sport.montant
	c=membre.cotisation.montant
	reserves = membre.reserve
	regl2 = regl + int(reserves)
	if regl2 >= p+s:
		if regl2 - (p+s)>=c:
			enc.tontine_presence = p
			enc.tontine_sport = s
			enc.tontine_cotisation = c
			enc.echec_presence = False
			enc.echec_sport = False
			enc.echec_cotisation = False
			enc.called = True
			enc.author = request.user
			enc.save()
			echec_cotisation = "False"
			echec_sport = "False"
			echec_presence = "False"
			context={'p': p, 's': s, 'c': c, 'echec_presence': echec_presence,
					'echec_sport': echec_sport, 'echec_cotisation': echec_cotisation}
		else:
			enc.tontine_presence = p
			enc.tontine_sport = s
			enc.tontine_cotisation = 0
			enc.echec_cotisation = True
			enc.echec_presence = False
			enc.echec_sport = False
			enc.called = True
			enc.author = request.user
			enc.save()
			echec_cotisation = "True"
			echec_sport = "False"
			echec_presence = "False"
			context={'p': p, 's': s, 'c': 0, 'echec_presence': echec_presence,
					'echec_sport': echec_sport, 'echec_cotisation': echec_cotisation}
	else:
		enc.echec_presence = True
		enc.echec_sport = True
		enc.echec_cotisation = True
		enc.tontine_presence = 0
		enc.tontine_sport = 0
		enc.tontine_cotisation = 0
		enc.called = True
		enc.author = request.user
		enc.save()
		echec_cotisation = "True"
		echec_sport = "True"
		echec_presence = "True"
		context={'p': 0, 's': 0, 'c': 0, 'echec_presence': echec_presence,
				'echec_sport': echec_sport, 'echec_cotisation': echec_cotisation}
	


	encs = Encaissement.objects.filter(seance=sea)
	totals = sum([x.reglement for x in encs])
	tontp = sum([x.tontine_presence for x in encs])

	tonts = sum([x.tontine_sport for x in encs])
	tontc = sum([x.tontine_cotisation for x in encs])
	
	context['totals'] = totals
	context['tontp'] = tontp
	context['tonts'] = tonts
	context['tontc'] = tontc
	context['reserve'] = max(0, regl2 - (p+s+c))
	context['impaye'] = max(0, (p+s+c)-regl2)
	print("voici la reserve mis à jour", regl2 - (p+s+c))
	return JsonResponse(context)


# Fermeture de session
@staff_member_required
def close_session(request, id):
	s = get_object_or_404(Seance, pk=id)
	encs = Encaissement.objects.filter(seance=s)
	s.total_encais = sum([x.reglement for x in encs])
	s.total_presence = sum([x.tontine_presence for x in encs])
	s.total_sport = sum([x.tontine_sport for x in encs])
	s.total_tontine = sum([x.tontine_cotisation for x in encs])
	for enc in encs:
		# echec présence
		if enc.echec_presence:
			s.nbechec_presence +=1
			s.mtechec_presence += enc.sanction_presence
		if enc.echec_sport:
			s.nbechec_sport +=1
			s.mtechec_sport += enc.sanction_sport
		if enc.echec_cotisation:
			s.nbechec_cotisation +=1
			s.mtechec_cotisation += enc.sanction_tontine
			if not Sanction.objects.filter(seance=s, membre=enc.membre).exists():
				v=enc.sanction_tontine
				w = enc.sanction_presence
				cons = Consigne.objects.filter(membre=enc.membre, date_consigne=s.date_seance)
				if cons.exists():
					mtcot = enc.membre.cotisation.montant
					cs = sum([h.montant_consigne for h in cons])
					csm= cons.first()
					if cs >= mtcot:
					    w=0
					    v=0
				date_franchise = enc.seance.exercice_tontine.franchise
				if date_franchise.date() >= s.date_seance:
					w=0
					v=0


				create_s= Sanction(seance=s, membre=enc.membre, valeur_sanction_tontine=v,
					valeur_sanction_presence=w)
				create_s.save()
	s.closed = True
	s.save()
	context={'s': s}
	messages.info(request, f'La séance du {s.date_seance} a été correctement clôturée !!!') 
	return render(request, 'tontine/home.html', context)

@login_required
def contributionhistory(request):
	if request.user.is_staff:
		encaissements = Encaissement.objects.filter(seance__exercice_tontine__is_active=True).order_by('-seance')
		#print(type(encaissements))
	else:
		try:
			m = request.user.membre
			encaissements = Encaissement.objects.filter(seance__exercice_tontine__is_active=True, membre=m).order_by('-seance')
		except Exception as e:
			encaissements = []
	reglement = sum([x.reglement for x in encaissements])
	tontine_presence = sum([x.tontine_presence for x in encaissements])
	tontine_sport = sum([x.tontine_sport for x in encaissements])
	tontine_cotisation = sum([x.tontine_cotisation for x in encaissements])
	sanction_sport = sum([x.sanction_sport for x in encaissements])
	sanction_presence = sum([x.sanction_presence for x in encaissements])
	sanction_cotisation = sum([x.sanction_tontine for x in encaissements])
	total_sanction = int(sanction_sport) + int(sanction_presence) + int(sanction_cotisation)
	total = tontine_presence + tontine_sport + tontine_cotisation
	context = {'encaissements': encaissements, 'title':"contributionhistory",
				"tontine_cotisation": tontine_cotisation, "tontine_sport": tontine_sport,
				"tontine_presence": tontine_presence, "reglement": reglement,
				"sanction_cotisation": sanction_cotisation, "sanction_presence":sanction_presence,
				"sanction_sport":sanction_sport, "total_sanction": total_sanction,
				"total": total}
	
	return render(request, 'tontine/contributionhistory.html', context)

# display sanction
@login_required
def sanction(request):
	if request.user.is_staff:
		listsanction = [obj for obj in Sanction.objects.all() if obj.is_active]
	else:
		try:
			m = request.user.membre
			listsanction = [obj for obj in Sanction.objects.filter(membre=m) if obj.is_active]
		except Exception as e:
			listsanction = []
	context = {"listsanction": listsanction}
	return render(request, 'tontine/sanction.html', context)


# paiement sanction cotisation
@staff_member_required
def paiement_sanction_tontine(request):
	# mId id of target row
	mId=request.POST.get('mId')
	r=request.POST.get('r_sc'+mId)
	regl = int(r)
	# recupere la sanction
	penalite = get_object_or_404(Sanction, pk=mId)
	penalite.regl_sanc_tontine = regl
	penalite.date_paiement_sc = timezone.now()
	penalite.save()
	context = {'paye': regl}
	return JsonResponse(context)

# paiement sanction présence
@staff_member_required
def paiement_sanction_presence(request):
	# mId id of target row
	mId=request.POST.get('mId')
	r=request.POST.get('r_sp'+mId)
	regl = int(r)
	# recupere la sanction
	penalite = get_object_or_404(Sanction, pk=mId)
	penalite.regl_sanc_presence = regl
	penalite.date_paiement_sp = timezone.now()
	penalite.save()
	context = {'paye_sp': regl}
	return JsonResponse(context)




@staff_member_required
def session_report(request):
	seances = [obj for obj in Seance.objects.filter(closed=True) if obj.tontine_is_active]
	context = {'seances': seances}
	return render(request, 'tontine/rapportsession.html', context)






#
def seance_detail(request, id):
	s=get_object_or_404(Seance, pk=id)
	d = s.date_seance

	benpres = BeneficiairePresence.objects.filter(seance=s)
	total_benpres = sum([m.montant for m in benpres])
	total_enchere_presence = sum([m.enchere for m in benpres])

	bencot = BeneficiaireTontine.objects.filter(seance=s)
	total_bencot = sum([m.montant for m in bencot])
	total_enchere_tontine = sum([m.frais_boissons for m in bencot])

	bank_jour = [b for b in EncaissementBank.objects.all() if b.date.date()==d]

	bank_entree = [be for be in bank_jour if be.operation == 'DEPÔT']

	bank_retrait = [br for br in bank_jour if br.operation == 'RETRAIT']

	total_banke = sum([b.montant for b in bank_entree])
	total_bankr = sum([b.montant for b in bank_retrait])

	# 
	cpt_association = [p for p in CompteAssociation.objects.all() if p.date.date()==d]
	entree_cpt_ass = [eca for eca in cpt_association if eca.operation == 'ENTREE']
	total_entree_cpt_ass = sum([p.montant for p in entree_cpt_ass])

	sortie_cpt_ass = [eca for eca in cpt_association if eca.operation == 'SORTIE']
	total_sortie_cpt_ass = sum([p.montant for p in sortie_cpt_ass])

	pret_bank_jour = [p for p in PretBank.objects.all() if p.date_pret.date()==d]
	total_pret = sum([p.montant for p in pret_bank_jour])

	remb_pret_jour = [p for p in RemboursementPretBank.objects.all() if p.date_remboursement.date()==d]
	total_remb = sum([r.montant for r in remb_pret_jour])
	context = {'s': s, 'date': d, 'bank_entree': bank_entree, 'bank_retrait': bank_retrait,
				'benpres': benpres,
				'total_benpres': total_benpres,
				'total_enchere_presence': total_enchere_presence,
				'bencot': bencot,
				'total_bencot': total_bencot,
				'total_enchere_tontine': total_enchere_tontine,
				 'pret_bank_jour':pret_bank_jour,
				 'remb_pret_jour': remb_pret_jour,
				 'total_banke': total_banke,
				 'total_bankr': total_bankr,
				 'total_remb': total_remb,
				 'total_pret': total_pret,
				 'entree_cpt_ass': entree_cpt_ass,
				 'sortie_cpt_ass': sortie_cpt_ass,
				 'total_entree_cpt_ass': total_entree_cpt_ass,
				 'total_sortie_cpt_ass': total_sortie_cpt_ass}
	return render(request, 'tontine/seance_detail.html', context)








# Création d'un bénéficiare cotisation
@staff_member_required
def creer_beneficiaire_tontine(request):
    context = {}
    membres = Membre.objects.filter(cotisation_bool=True).order_by("nom")
    context['membres']= membres
    if request.method == "POST":
        form = BeneficiaireTontineForm(request.POST)
        if form.is_valid():
            membre = form.cleaned_data['membre']
            amount = form.cleaned_data['montant']
            avaliseur = form.cleaned_data['avaliseur']
            form.instance.author = request.user
            form.save()
            messages.info(request, f'{membre.nom} a bénéficié {amount} XAF !!!')
            return redirect('creer_beneficiaire')

    else:
        if request.GET.get('membre'):
            params = request.GET.get('membre')
            membre = get_object_or_404(Membre, pk=params)
            context['membre']= membre
            form = BeneficiaireTontineForm(initial={'membre': membre,})
            hist = BeneficiaireTontine.objects.filter(seance__exercice_tontine__is_active=True, membre=membre,)    
            penalites = Sanction.objects.filter(seance__exercice_tontine__is_active=True, membre=membre)
            prets = PretBank.objects.filter(membre=membre, freeze=False)
            penalite = sum([pen.valeur_sanction_tontine for pen in penalites if pen.sanction_tontine_paye == 0])
            solde = sum([h.montant for h in hist])
            pretarembourser = sum([p.reste_a_rembourser for p in prets])
            context['penalite']= int(penalite)
            context['solde']= int(solde)
            context['pretarembourser']= int(pretarembourser)
        else:
            form = BeneficiaireTontineForm()

    context['form'] = form
        
    return render(request, 'tontine/beneficiaire_tontine.html', context)



# Création d'un bénéficiare présence
@staff_member_required
def creer_beneficiaire_presence(request):
    context = {}
    deja_beneficies = BeneficiairePresence.objects.filter(seance__exercice_presence__is_active=True).values('membre')
    membres = Membre.objects.filter(presence_bool=True).order_by("nom").exclude(id__in=deja_beneficies)
    context['membres']= membres 
    if request.method == "POST":
        form = BeneficiairePresenceForm(request.POST)
        if form.is_valid():
            membre = form.cleaned_data['membre']
            amount = form.cleaned_data['montant']
            form.instance.author = request.user
            form.save()
            messages.info(request, f'{membre.nom} a bénéficié {amount} XAF !!!')
            return redirect('creer_beneficiaire_presence')

    else:
        if request.GET.get('membre'):
        	params = request.GET.get('membre')
        	membre = get_object_or_404(Membre, pk=params)
        	context['membre']= membre
        	form = BeneficiairePresenceForm(initial={'membre': membre,})
        	hist = Encaissement.objects.filter(seance__exercice_presence__is_active=True, membre=membre) 

        	if ExercicePresence.objects.filter(is_active = True).exists():
        		exercice = ExercicePresence.objects.filter(is_active = True).first()
        		date_debut_exercice = exercice.date_debut
        		redirect('home')

        	benefice = BeneficiairePresence.objects.filter(seance__exercice_presence__is_active=True, membre=membre)
        	nbre = len(benefice)
        	penalite_disciplinaires = SanctionDisciplinaire.objects.filter(membre=membre)
        	penalite_consignes = Consigne.objects.filter(membre=membre, date_consigne__gte = date_debut_exercice)
        	penalites = Sanction.objects.filter(seance__exercice_presence__is_active=True, membre=membre)
        	prets = PretBank.objects.filter(membre=membre, freeze=False)
        	penalite = sum([pen.valeur_sanction_presence for pen in penalites if pen.sanc_presence_paye == 0])
        	penalite_disciplinaire = sum([pen.montant for pen in penalite_disciplinaires if pen.sanction_paye == 0])
        	penalite_consigne = sum([pen.penalite_consigne for pen in penalite_consignes if pen.consigne_paye == 0])
        	solde = sum([h.tontine_presence for h in hist])
        	pretarembourser = sum([p.reste_a_rembourser for p in prets])
        	context['penalite']= penalite
        	context['penalite_disciplinaire']= penalite_disciplinaire
        	context['penalite_consigne']= penalite_consigne
        	context['solde']= solde
        	context['nbre']= nbre
        	context['pretarembourser']= pretarembourser
        else:
            form = BeneficiairePresenceForm()
    context['form'] = form
        
    return render(request, 'tontine/beneficiaire_presence.html', context)

# Historique BENEFICIARE PRESENCE
@login_required
def beneficiairepresencehistory(request):
	if request.user.is_staff:
		bch = BeneficiairePresence.objects.filter(seance__exercice_presence__is_active=True)
	else:
		try:
			m=request.user.membre
			bch=BeneficiairePresence.objects.filter(membre=m, seance__exercice_presence__is_active=True)
		except Exception as e:
			bch=[]
	context = {'bch': bch}
	return render(request, "tontine/beneficiairepresencehistory.html", context)





#Création des avaliseurs
@staff_member_required
def creer_avaliseur(request):
    context = {}
    membres = Membre.objects.all().order_by("nom")
    if request.method == "POST":
        form = AvaliseurForm(request.POST)
        if form.is_valid():
        	aval = form.save(commit=False)
        	membre = form.cleaned_data['membre']
        	aval.author = request.user
        	aval.save()
        	messages.info(request, f'{membre.nom} peut être desormais avaliseur !!!')
        	return redirect('creer_beneficiaire_tontine')
        else:
        	context = {'form': form, 'membres': membres}
        	return render(request, 'tontine/avaliseur.html', context)
    else:
        if request.GET.get('membre'):
            params = request.GET.get('membre')
            membre = get_object_or_404(Membre, pk=params)
            context['membre']= membre
            form = AvaliseurForm(initial={'membre': membre})
            list_beneficier = BeneficiaireTontine.objects.filter(membre=membre)
            cap_beneficier = sum([value.montant for value in list_beneficier])
            avaliseur = Avaliseur.objects.filter(membre=membre).first()
            list_avaliser = BeneficiaireTontine.objects.filter(avaliseur=avaliseur)
            sum_charge_des_avalises = sum([value.charge for value in list_avaliser])
            solde = membre.cotisation.montant * 52 - cap_beneficier - sum_charge_des_avalises
            
        else:
            solde=0
            form = AvaliseurForm()
        context = {'form': form, 'membres': membres, 'solde': solde}
        return render(request, 'tontine/avaliseur.html', context)


# profil avaliseur et risque
@login_required
def profil_avaliseur(request):
	context = {}
	if request.user.is_staff:
		membres = Membre.objects.all().order_by("nom")
		context['membres']= membres
	else:
		if Membre.objects.filter(user=request.user).exists():
			membres = Membre.objects.filter(user=request.user)
			context['membres']= membres

	if request.GET.get('membre'):
		params = request.GET.get('membre')
		membre = get_object_or_404(Membre, pk=params)
		avaliseur = Avaliseur.objects.filter(membre=membre).first()
		mes_avalises = BeneficiaireTontine.objects.filter(avaliseur=avaliseur, seance__exercice_tontine__is_active=True)
		encaissements = Encaissement.objects.filter(membre__in=[c.membre for c in mes_avalises], seance__exercice_tontine__is_active=True).filter(echec_cotisation=True)
		context['membre']= membre
		context['mes_avalises'] = mes_avalises
		context['encaissements']= encaissements

	return render(request, 'tontine/profil_avaliseur.html', context)



# Historique BENEFICIARE COTISATION
@login_required
def beneficiairecotisationhistory(request):
	if request.user.is_staff:
		bch = BeneficiaireTontine.objects.filter(seance__exercice_tontine__is_active=True)
	else:
		try:
			m = request.user.membre
			bch = BeneficiaireTontine.objects.filter(seance__exercice_tontine__is_active=True, membre=m)
		except Exception as e:
			bch=[]
	context = {'bch': bch}
	return render(request, "tontine/beneficiairecotisationhistory.html", context)



# Formulaire des entrées sorties du compte d'association
@staff_member_required
def compte_association(request):
	data = CompteAssociation.objects.all()
	sum_entree = sum([x.montant for x in data if x.operation=='ENTREE'])
	sum_sortie = sum([x.montant for x in data if x.operation=='SORTIE'])
	solde = sum_entree - sum_sortie
	if request.method == "POST":
		form = CompteAssociationForm(request.POST)
		if form.is_valid():
			operation = form.cleaned_data['operation']
			amount = form.cleaned_data['montant']
			form.instance.author = request.user
			form.save()
			messages.info(request, f'{operation} de {amount} XAF dans le compte d\'association !!!')
			return redirect('compte_association')
	else:
		form = CompteAssociationForm()


	context = {'form': form, 'solde': solde}

	return render(request, "tontine/compteassociation.html", context)

@staff_member_required
def comptehistory(request):
	datas = CompteAssociation.objects.all()
	context = {'datas': datas}
	return render(request, "tontine/comptehistory.html", context)




# Gestion des sanctions disciplinaire
@staff_member_required
def sanction_disciplinaire(request):
	context = {}
	membres = Membre.objects.all().order_by("nom")
	if request.method == "POST":
		form = SanctionDisciplinaireForm(request.POST)
		if form.is_valid():
			membre = form.cleaned_data['membre']
			amount = form.cleaned_data['montant']
			form.instance.author = request.user
			form.save()
			messages.info(request, f'sanction de {amount} XAF pour {membre.nom} bien enregistrée  !!!')
			return redirect('sanction_disciplinaire')
	else:
		if request.GET.get('membre'):
			params = request.GET.get('membre')
			membre = get_object_or_404(Membre, pk=params)
			context['membre']= membre
			form = SanctionDisciplinaireForm(initial={'membre': membre, 'date': timezone.now()})
		else:
			form = SanctionDisciplinaireForm()
        
	context['membres']= membres
	context['form']= form
	return render(request, 'tontine/sanctiondisciplinaire.html', context)


@login_required
def history_disciplinaire(request):
	if request.user.is_staff:
		listsanction = SanctionDisciplinaire.objects.all()
	else:
		try:
			m=request.user.membre
			listsanction = SanctionDisciplinaire.objects.filter(membre=m)
		except Exception as e:
			listsanction = []
		
	context = {'listsanction': listsanction}
	return render(request, "tontine/disciplinehistory.html", context)

# paiement sanction disciplinaire
@staff_member_required
def paiement_sanction_disciplinaire(request):
	# mId id of target row
	mId=request.POST.get('mId')
	r=request.POST.get('r'+mId)
	regl = int(r)
	# recupere la sanction
	penalite = get_object_or_404(SanctionDisciplinaire, pk=mId)
	penalite.reglement = regl
	penalite.date_paiement = timezone.now()
	penalite.save()
	context = {'paye': regl}
	return JsonResponse(context)




# Gestion de contribution individuelle

@staff_member_required
def create_libellecontrib(request):
    context = {}
    if request.method == "POST":
        form = LibelleContributionForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle']
            montant = form.cleaned_data['minimum']
            form.instance.author = request.user
            form.save()
            messages.info(request, f'{libelle}: Contribution individuelle {montant}')
            return redirect('post_create_libellecontrib')
    else:
        form = LibelleContributionForm()

    context['form'] = form
    return render(request, 'tontine/libellecontrib.html', context)


@login_required
def post_create_libellecontrib(request):
	
	for libelle in LibelleContribution.objects.all():
		if not ContributionIndividuelle.objects.filter(motif=libelle).exists():
			for m in Membre.objects.all():
				row = ContributionIndividuelle(motif = libelle,
				membre = m,
				)
				row.save()
	
	listcontrib_ind = LibelleContribution.objects.all().order_by("-created")
	context= {'listcontrib_ind': listcontrib_ind}
	return render(request, 'tontine/post_create_libellecontrib.html', context)

@login_required
def	create_contrib_ind(request, id):
	motif = get_object_or_404(LibelleContribution, pk=id)
	if request.user.is_staff:
		datas = ContributionIndividuelle.objects.filter(motif=motif).order_by("-created")
	else:
		try:
			m= request.user.membre
			datas = ContributionIndividuelle.objects.filter(motif=motif, membre=m).order_by("-created")
		except Exception as e:
			datas = []
	lib = motif.libelle
	context={'datas': datas, 'lib': lib}
	return render(request, 'tontine/contrib_ind.html', context) 



# paiement contribution individuelle
@staff_member_required
def versement_contrib_ind(request):
	# mId id of target row
	mId=request.POST.get('mId')
	r=request.POST.get('r'+mId)
	regl = int(r)
	versement = get_object_or_404(ContributionIndividuelle, pk=mId)
	versement.reglement = regl
	versement.date_reglement = timezone.now()
	versement.author = request.user
	versement.save()
	context = {'paye': regl}
	return JsonResponse(context)






# Gestion des consignes
@staff_member_required
def consigne(request):
    context = {}
    membres = Membre.objects.all().order_by("nom")
    if request.method == "POST":
        form = ConsigneForm(request.POST)
        if form.is_valid():
            membre = form.cleaned_data['membre']
            montantc = form.cleaned_data['montant_consigne']
            form.instance.author = request.user
            form.save()
            messages.info(request, f'{membre.nom} a déposé une consigne de {montantc} !!!') 
            return redirect('consigne')
    else:
        if request.GET.get('membre'):
            params = request.GET.get('membre')
            membre = get_object_or_404(Membre, pk=params)
            context['membre']= membre
            form = ConsigneForm(initial={'membre': membre, 'date_consigne': timezone.now()})       
        else:
            form = ConsigneForm()
        
    context['membres']= membres
    context['form']= form
    return render(request, 'tontine/consigne.html', context)

@login_required
def consignehistory(request):
	if request.user.is_staff:
		listconsignes = Consigne.objects.all()
	else:
		try:
			m = request.user.membre
			listconsignes=Consigne.objects.filter(membre=m)
		except Exception as e:
			listconsignes = []
		
	context = {'listconsignes': listconsignes}
	return render(request, "tontine/consignehistory.html", context)

# paiement pénalité consigne
@staff_member_required
def paiement_penalite_consigne(request):
	# mId id of target row
	mId=request.POST.get('mId')
	r=request.POST.get('r'+mId)
	regl = int(r)
	# recupere la sanction
	penalite = get_object_or_404(Consigne, pk=mId)
	penalite.reglement = regl
	penalite.date_paiement = timezone.now()
	penalite.save()
	context = {'paye': regl}
	return JsonResponse(context)

