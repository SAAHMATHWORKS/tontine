from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from tontine.models import *
# Create your views here.

def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, You can Login Now!')
            return redirect('login')
    else:
        form=UserRegisterForm()
    context={'form': form}
    return render(request, "account/inscription.html", context)



@login_required
def profile(request):
    if not Membre.objects.filter(user=request.user).exists():
        context = {'profil': 'notok'}
    else:
        nb_seances = Seance.objects.filter(exercice_tontine__is_active=True).count()
        encs = [obj for obj in Encaissement.objects.filter(membre=request.user.membre) if obj.tontine_is_active]
        reglement = sum([x.reglement for x in encs])
        tontine_presence = sum([x.tontine_presence for x in encs])
        tontine_sport = sum([x.tontine_sport for x in encs])
        tontine_cotisation = sum([x.tontine_cotisation for x in encs])
        sanction_sport = sum([x.sanction_sport for x in encs])
        sanction_presence = sum([x.sanction_presence for x in encs])
        sanction_cotisation = sum([x.sanction_tontine for x in encs])
        total_sanction = int(sanction_sport) + int(sanction_presence) + int(sanction_cotisation)
        total = tontine_presence + tontine_sport + tontine_cotisation
        context = {'encs': encs, 'nb_seances': nb_seances, 'total': total,
                    "tontine_cotisation": tontine_cotisation, "tontine_sport": tontine_sport,
                    "tontine_presence": tontine_presence, "reglement": reglement,
                    "sanction_cotisation": sanction_cotisation, "sanction_presence":sanction_presence,
                    "sanction_sport":sanction_sport, "total_sanction": total_sanction,
                    'profil': 'ok'}
    #penalites = [obj for obj in Sanction.objects.filter(membre=request.user.membre) if obj.is_active]

    return render(request, 'account/profile.html', context)