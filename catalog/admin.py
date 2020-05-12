from django.contrib import admin
from catalog.models import Produit,Client,Selection


class ClientAdmin(admin.ModelAdmin):
    
    list_display = ('user','adresse','nombre_personnes','document')
admin.site.register(Client, ClientAdmin)


class ProduitAdmin(admin.ModelAdmin):
    
    list_display = ('nom','type_produit','id_p')
admin.site.register(Produit,ProduitAdmin)


class SelectionAdmin(admin.ModelAdmin):
    
    list_display = ('choix',)
admin.site.register(Selection,SelectionAdmin)

