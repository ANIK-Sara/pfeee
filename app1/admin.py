from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User ,PharmaCommandes,Contact,Messagerie, InfosPatient , Livreur ,  Medecin , Pharmacie , Patient , Produit_Prescris , Ordonnance , Produit, Admin2 , Commande
# Register your models here.
admin.site.register(User),
admin.site.register(Medecin),
admin.site.register(Pharmacie),
admin.site.register(Messagerie) 
admin.site.register(Patient),
admin.site.register(Admin2),
admin.site.register(Livreur),
admin.site.register(Contact),
admin.site.register(InfosPatient),
admin.site.register(Produit),
admin.site.register(Commande),
admin.site.register(Produit_Prescris),
admin.site.register(Ordonnance),
admin.site.register(PharmaCommandes),