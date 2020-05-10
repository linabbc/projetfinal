from catalog.models import Selection,Produit,Client
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import InscriptionForm,CommandeForm,PanierForm,Info
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from datetime import date
from time import strftime
from django.contrib.auth.models import User


def accueil(request):
    """View function for home page of site."""

    inscription = 'inscription'
    connexion = 'connexion'
    informations = 'informations'

#    
    context = {
        'inscription': inscription,
        'connexion': connexion,
        'informations': informations,
    }
    
#    messages.success(request,'Le produit le plus vendu est : ' + Stat(request))
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'accueil.html', context=context)
  
hist = []   
#historique = []
 
def commander(request):
    L = Apriori()
    mot = ""
    i = 0
    for n in L:
        if(i == len(L) - 1):
            mot += ' ' + str(Produit.objects.get(id_p = n)) + '.'
        
        else:
            mot += ' ' + str(Produit.objects.get(id_p = n)) + ','
            i += 1

            
    messages.info(request,'Voici le panier du jour:' + mot)
    messages.info(request,'Cochez la case si vous voulez commander ce panier.')                
    selection = Selection()
    if request.method == 'POST':
        form2 = PanierForm(request.POST)
        if form2.is_valid():
            if form2.cleaned_data['choix'] == '1':
                selection.choix = Apriori()
                hist.append((date.today(),selection.choix))
                selection.choix.append(request.user.username)
                selection.save()
            else:
                return redirect('choix_produit')
            return redirect('accueil')
    else:
#        form1 = CommandeForm(initial={})
        form2 = PanierForm(initial={})

    context = {
        'form2':form2
    }
    return render(request, 'catalog/panier.html', context)

def historique(request):
    for i in range(len(hist)):
        date,choix=hist[i]
        if request.user.username == str(choix[-1]):
            mot = ""
            i = 0
            for n in choix[0:-1]:
                if(i == len(choix) - 2):
                    mot += ' ' + str(Produit.objects.get(id_p = n)) + '.'
        
                else:
                    mot += ' ' + str(Produit.objects.get(id_p = n)) + ','
                    i += 1
            messages.success(request,'Le ' + str(date) + ', vous avez commandé: '+ mot)
    return render(request,'catalog/historique.html',{})

def documents(request):
    return render(request,'catalog/documents.html',{})
  
def Admin(request):
    return redirect('/admin')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accueil'))
    
def renew_inscription(request):
    form = InscriptionForm()
    form2 = Info()
    client = Client()
    if request.method == 'POST':
        form =  InscriptionForm(request.POST, request.FILES or None)
        form2 = Info(request.POST)
        if form.is_valid() and form2.is_valid():
            form.save()
            user = form.cleaned_data['username']
            client.user = user
            client.document = form.cleaned_data['document']
            client.adresse = form2.cleaned_data['adresse']
            client.nombre_personnes = form2.cleaned_data['nombre_personnes']
            messages.success(request,'Vous êtes maintenant inscrit(e) ' + user + ' !')
            client.save()
            return redirect('user_login')
            
    context = {'client':client,'form':form,'form2':form2}
    return render(request, 'catalog/inscription.html',context)
    
def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('accueil')
        else:
            messages.info(request,'Username or password in incorrect')
    context = {}
    return render(request,'catalog/user_login.html',context)


def Erase (Dico,seuil):
        l = list(Dico.keys())
        for key in l:
            if (Dico[key]<seuil): Dico.pop(key)
        return Dico
    
def Apriori():
        a = [list(q.values()) for q in Selection.objects.values()]
        queryset = [eval(a[i][1]) for i in range(len(a))]
        T = []
        for commande in queryset:
            T.append(commande[0:len(commande)-1])
            
        Id = []
        Compteur = []
        
        for t in T :
            for produit in t:
                if produit in Id : Compteur[Id.index(produit)] += 1
                else :
                    Id.append(produit)
                    Compteur.append(1)
            
        
        nb_prdt_moyen = sum(Compteur)/len(queryset)
        seuil = nb_prdt_moyen - 1
        Dic1 = dict(zip(Id,Compteur))
        Erase(Dic1,seuil)
        
        Dic2 = {}
        
        for i in Dic1:
            for j in Dic1:
                if(i < j) : Dic2[(i,j)] = 0
        
        #Si les deux elements du doublets sont dans la transaction, on compte +1
        for double in Dic2:
            for i in T:
                if ((double[0] in i) and (double[1] in i)) :
                    Dic2[double]+=1
                    
        Erase(Dic2,seuil)
                    
        Dic3 = {}
        
        #Formation des triplets
        for elm in Dic2 :
            a,b = elm[0],elm[1]
            for k in Dic2 :
                if (a == k[0] and b != k[1]) :
                    if((a,k[1],b) not in Dic3) : Dic3[(a,b,k[1])] = 0
                
        #Comptage des triplets dans les transactions        
        for triple in Dic3:
            for i in T:
                if ((triple[0] in i) and (triple[1] in i) and (triple[2] in i)) :
                    Dic3[triple]+=1
    
    
        for k in Dic3.keys() :
            if (Dic3[k] == max(Dic3.values())) : return list(k)

def articles(request):
    selection = Selection()
    form = CommandeForm()
    today = date.today()
    if request.method == 'POST':
        form =  CommandeForm(request.POST)
        if form.is_valid():
#            form.save()
            selection.choix = form.cleaned_data['choix']
            hist.append((today,selection.choix))
            selection.choix.append(request.user.username)
            selection.save()
            return redirect('accueil')
            
    context = {'form':form}
    return render(request, 'catalog/produit_list.html',context)



#def Stat(request):
#    p = Produit_vendu()
#    mot = str(Produit.objects.get(id_p = p))
#    return mot
#    return render(request,'catalog/accueil.html',{})