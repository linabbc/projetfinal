from django.urls import path
from . import views
from django.urls import include

import os
PROJECT_DIR=os.path.dirname(__file__)

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.renew_inscription, name='inscription'),
    path('commande/', views.commander, name='commande'),
    path('user_login/',views.user_login,name='user_login'),
    path('historique/',views.historique,name='historique'),
    path('documents/',views.documents,name='documents'),
    path('choix_produit/',views.articles,name='choix_produit'),

]

