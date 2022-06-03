from django.urls import path
from . import views

urlpatterns = [
    path('insert/', views.bankoperation, name='bankoperation'),
    path('pret/create/', views.pretbank, name='pretbank'),
    path('pret/reconduction/<int:id>/', views.reconduction, name='reconduction'),
    path('listpret/', views.listpret, name='listpret'),
    path('pret/freeze/<int:id>/', views.freeze, name='freeze'),
    path('loanhistory/', views.loanhistory, name='loanhistory'),
    path('refundhistory/', views.refundhistory, name='refundhistory'),
    path('bankhistory/', views.bankhistory, name='bankhistory'),
    path('rembpretbank/', views.rembpretbank, name='rembpretbank'),
]