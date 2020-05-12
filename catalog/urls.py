from django.urls import path
from . import views

import os
PROJECT_DIR=os.path.dirname(__file__)

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.renew_inscription, name='inscription'),
    path('commande/', views.commander, name='commande'),
    path('user_login/',views.user_login,name='user_login'),
    path('historique/',views.historique,name='historique'),
    path('mesinfos/',views.modif,name='mesinfos'),
    path('choix_produit/',views.articles,name='choix_produit'),
    path('modifications/',views.modifier,name='modifications'),
    path('contact/',views.contact,name='contact'),
]

