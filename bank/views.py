from django.shortcuts import render, redirect, get_object_or_404
from tontine.models import Membre
from .models import *
from.forms import BankForm, PretBankForm, RemboursementPretBankForm, PretBankiForm
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def bankoperation(request):
    context = {}
    membres = Membre.objects.all().order_by("nom")
    if request.method == "POST":
        form = BankForm(request.POST)
        if form.is_valid():
            membre = form.cleaned_data['membre']
            operation = form.cleaned_data['operation']
            amount = form.cleaned_data['montant']
            hist = EncaissementBank.objects.filter(membre=membre)
            solde = sum([h.value for h in hist])
            if operation == 'RETRAIT':
                if solde <= int(amount):
                    messages.warning(request, f'Le solde de  {membre.nom}, est insuffisant !!!')
                    return redirect('bankoperation')
            
            form.instance.author = request.user    
            form.save()
            messages.info(request, f'{membre.nom}  {operation}  {amount} FCFA !!!')
            return redirect('bankoperation')
    else:
        if request.GET.get('membre'):
            params = request.GET.get('membre')
            membre = get_object_or_404(Membre, pk=params)
            context['membre']= membre
            form = BankForm(initial={'membre': membre, 'date': timezone.now()})
            hist = EncaissementBank.objects.filter(membre=membre)
            if len(hist)>0:
                solde = sum([h.value for h in hist])
            else:
                solde=0
        else:
            solde=0
            form = BankForm()
        
    context['membres']= membres
    context['form']= form
    context['solde']= int(solde)
    return render(request, 'bank/banque.html', context)

@staff_member_required
def pretbank(request):
    context = {}
    membres = Membre.objects.all().order_by("nom")
    if request.method == "POST":
        form = PretBankForm(request.POST)
        if form.is_valid():
            membre = form.cleaned_data['membre']
            amount = form.cleaned_data['montant']
            form.instance.author = request.user
            form.save()
            messages.info(request, f'{membre.nom} a fait un prêt de {amount} !!!')
            return redirect('pretbank')
    else:
        
        if request.GET.get('membre'):
            params = request.GET.get('membre')
            context['params']= params
            membre = get_object_or_404(Membre, pk=params)
            context['membre']= membre
            form = PretBankForm(initial={'membre': membre, 'date_pret': timezone.now()})
            hist = EncaissementBank.objects.filter(membre=membre)
            solde = sum([h.value for h in hist])
            context['solde']= int(solde)
        else:
            form = PretBankForm()
        


    context['form']= form
    context['membres']= membres
    return render(request, 'bank/pretbank.html', context)



def reconduction(request, id):
    dette = get_object_or_404(PretBank, pk=id)
    if request.method == "POST":
        form = PretBankiForm(request.POST)
        if form.is_valid():
            membre = form.cleaned_data['membre']
            amount = form.cleaned_data['montant']
            form.instance.author = request.user
            form.save()
            messages.info(request, f'Reconduction de prêt pour {membre.nom} d\'un montant de {amount} FCFA !!!')
            return redirect('freeze', dette.id)
    else:
        form = PretBankiForm(initial={'montant': dette.reste_a_rembourser, 'membre': dette.membre,
                             'date_pret': dette.date_remboursement + timedelta(days=1)})

        context = {'form': form, 'dette': dette}

        return render(request, 'bank/reconduction.html', context)



def freeze(request, id):
    dette = get_object_or_404(PretBank, pk=id)
    dette.freeze = True
    dette.save()
    return render(request, 'bank/freeze.html')

@login_required
def listpret(request):
    if request.user.is_staff:
        pret1 = PretBank.objects.filter(freeze=False)
    else:
        try:
            m=request.user.membre
            pret1 = PretBank.objects.filter(membre=m, freeze=False)
        except Exception as e:
            pret1 = []
    prets = [x for x in pret1 if x.reste_a_rembourser>0]
    context = {'prets': prets}
    return render(request, "bank/listpret.html", context)


#Remboursement prêt bank
@staff_member_required
def rembpretbank(request):
    context = {}
    form = RemboursementPretBankForm()
    if request.method == "POST":
        form = RemboursementPretBankForm(request.POST)
        if form.is_valid():
            pretbank = form.cleaned_data['pretbank']
            amount = int(form.cleaned_data['montant'])
            pretbank.versement_remboursement+=amount
            pretbank.save()
            form.instance.author = request.user
            form.save()
            messages.info(request, f'{amount}fcfa de remboursement de prêt bien enregistré pour {pretbank.membre.nom}!!!')
            return redirect('rembpretbank')
    else:
        if request.GET.get('pretbankid'):
            params = request.GET.get('pretbankid')
            pretbank = get_object_or_404(PretBank, pk=params)
            membre = pretbank.membre
            reste_a_rembourser = pretbank.reste_a_rembourser
            context['reste_a_rembourser'] = reste_a_rembourser
            context['membre']= membre
            context['pretbankid']= pretbank
            form = RemboursementPretBankForm(initial={'pretbank': pretbank, 'date_remboursement': timezone.now()})
        else:
            form = RemboursementPretBankForm()
        
    context['form']= form
    return render(request, 'bank/rembpretbank.html', context)


# Historique prêt bancaire
@login_required
def loanhistory(request):
    if request.user.is_staff:
        prets = PretBank.objects.all()
    else:
        try:
            m = request.user.membre
            prets = PretBank.objects.filter(membre=m)
        except Exception as e:
            prets = []
    context = {'prets': prets}
    return render(request, "bank/loanhistory.html", context)


# Historique remboursement prêt
@login_required
def refundhistory(request):
    if request.user.is_staff:
        remboursements = RemboursementPretBank.objects.all()
    else:
        try:
            m=request.user.membre
            remboursements = RemboursementPretBank.objects.filter(pretbank__membre = m)
        except Exception as e:
            remboursements = []
    context = {'remboursements': remboursements}
    return render(request, "bank/refundhistory.html", context)



# Historique opération 
@login_required
def bankhistory(request):
    if request.user.is_staff:
        banks = EncaissementBank.objects.all()
    else:
        try:
            m = request.user.membre
            banks = EncaissementBank.objects.filter(membre=m)
        except Exception as e:
            banks=[]
    sum_depot_bank = sum([s.montant for s in banks if s.operation=='DEPÔT'])
    sum_retrait_bank = sum([s.montant for s in banks if s.operation=='RETRAIT'])
    sum_interet_bank = sum([s.montant for s in banks if s.operation=='INTERÊT'])

    solde = sum_depot_bank + sum_interet_bank - sum_retrait_bank
    context = {'banks': banks, 'sum_depot_bank': sum_depot_bank, 'sum_retrait_bank': sum_retrait_bank,
                'sum_interet_bank': sum_interet_bank, 'solde': solde}
    return render(request, "bank/bankhistory.html", context)