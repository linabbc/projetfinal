from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid # Ce module est nécessaire à la gestion des identifiants unique (RFC 4122) pour les copies des livres
from django.contrib.auth.models import AbstractBaseUser

class Produit(models.Model):
    """A typical class defining a model, derived from the Model class."""
    # Fields
    nom = models.CharField(max_length=50, help_text='Enter field documentation')
    medicament = 'medicament'
    cosmetique = 'cosmetique'
    viande = 'viande'
    poisson = 'poisson'
    produit_menager = 'produit ménager'
    legume = 'légume'
    fruit = 'fruit'
    boisson = 'boisson'
    epicerie = 'epicerie'
    type_produit_choices = [(medicament,'medicament'),(cosmetique,'cosmetique'),(viande,'viande'),(poisson,'poisson'),(produit_menager,'produit ménager'),(legume,'légume'),(fruit,'fruit'),(boisson,'boisson'),(epicerie,'epicerie'),]
    type_produit = models.CharField(max_length=100, choices=type_produit_choices)
    id_p = models.AutoField(primary_key = True)
    # Metadata
    class Meta: 
        ordering = ['type_produit']

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.nom

    
    
    
class Client(models.Model):
    """A typical class defining a model, derived from the Model class."""
    # Fields
    user = models.TextField(max_length=50)
    document = models.FileField(null=True,blank=True)
    adresse = models.CharField(max_length=500)
    nombre_personnes = models.IntegerField()

    class Meta:
        ordering = ['user']





class Selection(models.Model):

    choix = models.TextField(default = " ") 
    
    class Meta:
        ordering = ['choix']
        
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.choix
