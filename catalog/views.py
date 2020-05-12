from catalog.models import Selection,Produit,Client
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import InscriptionForm,CommandeForm,PanierForm,Info,ModifInfo,ModifierInfo,BesoinInfo
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date


def accueil(request):
    """View function for home page of site."""
    return render(request, 'accueil.html',{})
  
    

hist = []   
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
                selection.choix.append(request.user.username)
                selection.save()
                hist.append((date.today(),selection.choix))
            else:
                return redirect('choix_produit')
            return redirect('accueil')
    else:
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
            j = 0
            for n in choix[0:-1]:
                if(j == len(choix) - 2):
                    mot += ' ' + str(Produit.objects.get(id_p = n)) + '.'
        
                else:
                    mot += ' ' + str(Produit.objects.get(id_p = n)) + ','
                    j += 1
            messages.success(request,'Le ' + str(date) + ', vous avez commandé: '+ mot)
    return render(request,'catalog/historique.html',{})


def modif(request):
    if request.method == 'POST':
        form = ModifInfo(request.POST)
        form1 = BesoinInfo(request.POST)
        if form.is_valid()and form1.is_valid():
            if form.cleaned_data['modif']:
                return redirect('modifications')
            return redirect('mesinfos')
    else:
        form = ModifInfo(initial={})
        form1 = BesoinInfo(initial={})
    context = {
        'form':form,'form1':form1
    }
    return render(request, 'catalog/mesinfos.html', context)


def contact(request):
    return render(request,'catalog/contact.html')


def modifier(request): 
    if request.method == 'POST':
        form = ModifierInfo(request.POST)
        if form.is_valid():
            return redirect('mesinfos')
    else:
        form = ModifierInfo(initial={})
    context = {'form':form}
    return render(request,'catalog/modifications.html',context)
  
    
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
            client.adresse = form2.cleaned_data['adresse']
            client.document = form.cleaned_data['document']
            client.nombre_personnes = form2.cleaned_data['nombre_personnes']
            client.save()
            messages.success(request,'Vous êtes maintenant inscrit(e) ' + user + ' !')
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
            selection.choix = form.cleaned_data['choix']
            hist.append((today,selection.choix))
            selection.choix.append(request.user.username)
            selection.save()
            return redirect('accueil')
            
    context = {'form':form}
    return render(request, 'catalog/produit_list.html',context)



