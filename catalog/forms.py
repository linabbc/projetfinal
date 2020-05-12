from django import forms
from catalog.models import Client,Selection,Produit
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class InscriptionForm(UserCreationForm):
    last_name = forms.CharField(required = True, label = 'Nom')
    first_name = forms.CharField(required = True, label = 'Prénom')
    email= forms.EmailField(required = True, label = 'Email')
    document = forms.FileField(required = False, label = 'Document (facultatif)')

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','document')
       
        
class Connexion(forms.ModelForm):
    username = forms.CharField(required = True, label = 'Username')
    password = forms.CharField(required=True,label='Mot de passe',widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username','password',)


class Info(forms.ModelForm):
    adresse = forms.CharField(required = True,label ='Adresse')
    nombre_personnes = forms.IntegerField(required = True, label = 'Nombre de personnes dans le foyer')

    class Meta:
        model = Client
        fields = ('nombre_personnes','adresse')


class ModifInfo(forms.ModelForm):
    modif = forms.BooleanField(required=False,label='Modifier mes informations personnelles')
  
    class Meta:
        model = Client
        fields = ('modif',)


class BesoinInfo(forms.ModelForm):
    besoin = forms.CharField(required=False,label = 'Si vous avez des besoins particuliers, remplissez-ce champ. Nous traiterons votre demande dans les plus brefs délais')
   
    class Meta:
        model = Client
        fields = ('besoin',)
   
     
class ModifierInfo(forms.ModelForm):
    em = forms.EmailField(label='email',required=False)
    ad = forms.CharField(label='adresse',required=False)
    doc = forms.FileField(label='document',required=False)
  
    class Meta:
        model = Client
        fields = ('em','ad','doc')
    
    
def Produit_vendu():
        a = [list(q.values()) for q in Selection.objects.values()]
        queryset = [eval(a[i][1]) for i in range(len(a))]
    
        Id = []
        Compteur = []
    
        for t in queryset :
            for produit in t[0:-1]:
                if produit in Id : Compteur[Id.index(produit)] += 1
                else :
                    Id.append(produit)
                    Compteur.append(1)
    
        index = Compteur.index(max(Compteur))
        return Id[index]
   
    
def liste():
        l = []
        querySet = Produit.objects.all()
        index = Produit_vendu()
        for pdt in querySet:
            if eval(index) == pdt.id_p:
                l.append((pdt.id_p,pdt.nom + " ★"))
            else:
                l.append((pdt.id_p,pdt.nom))               
        return l


class CommandeForm(forms.ModelForm):           
    choix = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices = [(x) for x in liste()],required = False)
    class Meta:
        model = Selection
        fields = ('choix',)


class PanierForm(forms.ModelForm):
    choices = ((0,'non'),(1,'oui'))
    choix = forms.ChoiceField(choices = choices,widget=forms.RadioSelect,required = False,label = 'Panier')
    class Meta:
        model = Selection
        fields = ('choix',)
        
