from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #path('tontine/', views.tontine, name='tontine'),
    path('tontine/<int:id>/', views.tontine, name='tontine'),
    path('savedata/', views.savedata, name='savedata'),


    #Création d'une séance
    path('creer_seance/', views.create_session, name='create_session'),
    path('post_create_session/', views.post_create_session, name='post_create_session'),

    path('close_session/<int:id>/', views.close_session, name='close_session'),

    path('seance_detail/<int:id>/', views.seance_detail, name='seance_detail'),
    path('sanction/', views.sanction, name='sanction'),
    #path('create_sanction/<int:id>/', views.create_sanction, name='create_sanction'),
    path('session_report/', views.session_report, name='session_report'),
    path('paiement_sanction_tontine/', views.paiement_sanction_tontine, name='paiement_sanction_tontine'),
    path('paiement_sanction_presence/', views.paiement_sanction_presence, name='paiement_sanction_presence'),
    path('contributionhistory/', views.contributionhistory, name='contributionhistory'),

    #beneficiare tontine
    path('creer_beneficiaire_tontine/', views.creer_beneficiaire_tontine, name='creer_beneficiaire_tontine'),
    path('beneficiairecotisationhistory/', views.beneficiairecotisationhistory, name='beneficiairecotisationhistory'),

    #beneficiare présence
    path('creer_beneficiaire_presence/', views.creer_beneficiaire_presence, name='creer_beneficiaire_presence'),
    path('beneficiairepresencehistory/', views.beneficiairepresencehistory, name='beneficiairepresencehistory'),
    
    # Consigne
    path('consigne/', views.consigne, name='consigne'),
    path('consignehistory/', views.consignehistory, name='consignehistory'),
    path('paiement_penalite_consigne/', views.paiement_penalite_consigne, name='paiement_penalite_consigne'),

    #sanction disciplinaire
    path('sanction_disciplinaire/', views.sanction_disciplinaire, name='sanction_disciplinaire'),
    path('history_disciplinaire/', views.history_disciplinaire, name='history_disciplinaire'),
    path('paiement_sanction_disciplinaire/', views.paiement_sanction_disciplinaire, name='paiement_sanction_disciplinaire'),
    
 
    # Compte d'association
    path('compte_association/', views.compte_association, name='compte_association'),
    path('comptehistory/', views.comptehistory, name='comptehistory'),

    # profil avaliseur
    path('creer_avaliseur/', views.creer_avaliseur, name='creer_avaliseur'),
    path('profil_avaliseur/', views.profil_avaliseur, name='profil_avaliseur'),
 


    # contribution individuelle
    path('create_libellecontrib/', views.create_libellecontrib, name='create_libellecontrib'),
    path('contrib-individuelle/<int:id>/', views.create_contrib_ind, name='create_contrib_ind'),
    path('post_create_libellecontrib/', views.post_create_libellecontrib, name='post_create_libellecontrib'),
    #versement_contrib_ind
    path('versement_contrib_ind/', views.versement_contrib_ind, name='versement_contrib_ind'),

    path('historique-contrib-individuelle/', views.history_contrib_ind, name='history_contrib_ind'),
]