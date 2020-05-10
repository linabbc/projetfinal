from catalog.models import Produit, Client,Selection
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from catalog.forms import InscriptionForm,CommandeForm,Info,Connexion
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


#from django.views.decorators import csrf_exempt

def accueil(request):
    """View function for home page of site."""
#
#    # Generate counts of some of the main objects
#    num_books = Book.objects.all().count()
#    num_instances = BookInstance.objects.all().count()
#    
#    # Available books (status = 'a')
#    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
#    
#    # The 'all()' is implied by default.    
#    num_authors = Author.objects.count()
    inscription = 'inscription'
    connexion = 'connexion'
    informations = 'informations'

#    
    context = {
        'inscription': inscription,
        'connexion': connexion,
        'informations': informations,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'accueil.html', context=context)
# Create your views here.
#class LoanedProductsByUserListView(LoginRequiredMixin,ListView):
#    """Generic class-based view listing books on loan to current user."""
#    model = ProduitInstance
#    template_name ='catalog/inscription.html'
#    paginate_by = 10
#    
#    def get_queryset(self):
#        return ProduitInstance.objects.filter(commande=self.request.user).filter(status__exact='n')

#@permission_required('catalog.can_mark_returned')
#@csrf_exempt
def renew_inscription(request):
    client = Client()


    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form1 = InscriptionForm(request.POST)
        form2 = Info(request.POST)

        # Check if the form is valid:
        if form1.is_valid() and form2.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            nom = form1.cleaned_data['nom']
            prenom = form1.cleaned_data['prenom']
            client.adresse = form2.cleaned_data['adresse']
            email = form1.cleaned_data['email']
            client.nombre_personnes = form2.cleaned_data['nombre_personnes']
            mot_de_passe= form1.cleaned_data['mot_de_passe']
            username = form1.cleaned_data['username']
            user = User.objects.create_user(username=username,email=email,password=mot_de_passe,first_name=prenom,last_time=nom)
#            user.
            user.save()
            client.user = user
            client.save()

#            client.set_username(client.email)
##            client.set_password(client.mot_de_passe)
#            user = .create_user((client.email,client.mot_de_passe))
#            user.save()
#            user = authenticate(username = client.email,password = client.mot_de_passe,create_unknown_user=False)
#            login(request,user )
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('accueil'))

#     If this is a GET (or any other method) create the default form.
    else:
        form1 = InscriptionForm(initial={})
        form2 = Info(initial={})


    context = {
       'client': client,'form1':form1,'form2':form2
    }

    return render(request, 'catalog/inscription.html', context)

class ProduitListView(generic.ListView):
    model = Produit
    context_object_name = 'produit_list'   # your own name for the list as a template variable
    queryset = Produit.objects.order_by('nom')
    template_name = 'commande/produit_list.html'  # Specify your own template name/location
  
def commander(request):
    selection = Selection()
#    produits = Produit.objects.all()
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CommandeForm(request.POST)
#        produits = Produit.objects.all()
#        l = []
#        i = 1
        
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#            l = form.cleaned_data['produits']
#            for produit in produits:
            selection.choix = form.cleaned_data['choix']
            selection.choix.append(request.user.username)
#            l.append(a)
#                l.add(i,produit.nom)
#                if(form.data == True):
#                    selection.choix += produit.nom
#            client.nom = form.cleaned_data['nom']
#            client.prenom = form.cleaned_data['prenom']
#            client.adresse = form.cleaned_data['adresse']
#            client.email = form.cleaned_data['email']
#            client.nombre_personnes = form.cleaned_data['nombre_personnes']
#            selection.choix = str(a)
            selection.save()
            

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('accueil') )

#     If this is a GET (or any other method) create the default form.
    else:
        form = CommandeForm(initial={})

    context = {
        'form': form,
        'selection': selection,
    }

    return render(request, 'catalog/produit_list.html', context)
 
#list_p = Produit.objects.all()
#t = ()
#i = 1
#def login(request):
#    if request.method == 'POST':
#        username = request.POST.get('username')
#        password = request.POST.get('password')
#        user = authenticate(username = username,password=password)
#        if user:
#            if user.is_active:
#                login(request,user)
#                return HttpResponseRedirect(reverse('accueil'))
#            else:
#                return HttpResponse("Your account was inactive")
#        else:
#            print()
#    else:
#        return render(request,'catalog/login.html',{})
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accueil'))
    
def user_login(request):
    error = False
    if request.method == 'POST':
        form = Connexion(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user:
#                if user.is_active:
                login(request,user)
#                return HttpResponseRedirect(reverse('accueil'))
#                else:
#                    return HttpResponse("Your account was inactive.")
            else:
#                print("Someone tried to login and failed.")
#                print("They used username: {} and password: {}".format(username,password))
                error = True
    else:
        form = Connexion()
#
##
#    context = {
#                 'form':form,
#    }

    return render(request,'catalog/user_login.html',locals())
     
#def user_login(request):
#    if request.method == 'POST':
#        username = request.POST.get('username')
#        password = request.POST.get('password')
#        user = authenticate(username=username, password=password)
#        if user:
#            if user.is_active:
#                login(request,user)
#                return HttpResponseRedirect(reverse('accueil'))
#            else:
#                return HttpResponse("Your account was inactive.")
#        else:
#            print("Someone tried to login and failed.")
#            print("They used username: {} and password: {}".format(username,password))
#    else:
##         username = request.POST.get()
##         password = request.POST.get()
##
##
##         context = {
##      'username':username,'password':password
##    }
#
#         return render(request, 'catalog/user_login.html',{})

#@login_required
#def logout(request):
#    return HttpResponseRedirect(reverse('accueil'))
    

{% extends "base_generic.html" %}

{% block content %} 
  <h class="quarant">Quarant'In Need</h>
  {% if form.errors %}
    <p>Veuillez reessayer.</p>
  {% endif %}
  
  {% if next %}
    {% if user.is_authenticated %}
      <p>Your account doesn't have access to this page. To proceed,
      please login with an account that has access.</p>
    {% else %}
    {% endif %}
  {% endif %}
  
  <form method="post" action="{% url 'user_login' %}" class="connexion">
    {% csrf_token %}
    <table>
      <tr>
        <td>{{ form.username.label_tag }}</td>
        <td>{{ form.username }}</td>
      </tr>
      <tr>
        <td>{{ form.password.label_tag }}</td>
        <td>{{ form.password }}</td>
      </tr>
    </table>
    <input type="submit" value="Valider" />
    <input type="hidden" name="next" value="{{ next }}" />
  </form>
  
  
  
{% endblock %}

{% extends "base_generic.html" %}

{% block content %} 
  <h1>Se connecter</h1>

    {% if error %}
    <p><strong>Utilisateur inconnu ou mauvais de mot de passe.</strong></p>
    {% endif %}

    {% if user.is_authenticated %}
    Vous etes connecte, {{ user.username }} !
    {% else %}
    <form method="post" action=".">

      {% csrf_token %}
      {{ form.as_table }}
      <input type="submit" value="Se connecter" />
    </form>
    {% endif %}
{% endblock %}