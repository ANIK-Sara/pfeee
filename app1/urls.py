from django.urls import path 
from . import views
from .views import ProductDeleteView

urlpatterns = [
path('' , views.index , name='index'),
path('login/' , views.login_view , name='login_view'),
path('register/' , views.register , name='register'),
path('commande_details/<int:commande_id>/', views.commande_details, name='commande_details'),
path('commande_details_liv/<int:commande_id>/', views.commande_details_liv, name='commande_details_liv'),

path('livreur/' , views.livreur , name='livreur'),
path('livraison_terminee/' , views.livraison_terminee , name='livraison_terminee'),
 path('api/produit/<int:produit_id>/', views.get_produit, name='get_produit'),
    path('modifier_produit/', views.modifier_produit, name='modifier_produit'),
    # Autres URLs de votre application
path('deconnexion/', views.deconnexion, name='deconnexion'),
path('profile/', views.profile, name='profile'),
path('profileliv/', views.profileliv, name='profileliv'),
path('profilepatient/', views.profilepatient, name='profilepatient'),
path('profileadmin/', views.profileadmin, name='profileadmin'),
path('profilmed/', views.profilmed, name='profilmed'),
path('historique_medecin/', views.historique_medecin, name='historique_medecin'),
path('search_patient/', views.search_patient, name='search_patient'),
path('patient_ordonnances/', views.patient_ordonnances, name='patient_ordonnances'),
    path('pagedegarde/', views.page_de_garde, name='pagedegarde'),  # Chemin pour accéder à votre page de garde
    path('a_propos_de_nous/', views.a_propos, name='apropos'),

path('get_patient_details/', views.get_patient_details, name='get_patient_details'),

path('messagerie_pharmacie/', views.messagerie_pharmacie, name='messagerie_pharmacie'),
path('contact/', views.contactez_nous, name='contact'),
    path('messages-contact/', views.messages_contact, name='messages_contact'),
    path('messages_recus/', views.messages_recus, name='messages_recus'),
        path('envoyer_message/', views.envoyer_message, name='envoyer_message'),


path('repondre_message/', views.repondre_message, name='repondre_message'),
    path('messages_envoyes/', views.messages_envoyes, name='messages_envoyes'),
    path('get_message_details/', views.get_message_details, name='get_message_details'),
path('messages_recus_pharmacie/', views.messages_recus_pharmacie, name='messages_recus_pharmacie'),
path('repondre_message_medecin/<int:medecin_id>/' , views.repondre_message_medecin , name='repondre_message_medecin'),
path('confirmation_contact/', views.confirmation_contact, name='confirmation_contact'),
    path('creer_ordonnance/', views.creer_ordonnance, name='creer_ordonnance'),
    path('messagerie_medecin/', views.messagerie_medecin, name='messagerie_medecin'),
    path('messagerie_pharmacie/', views.messagerie_pharmacie, name='messagerie_pharmacie'),

path('historique_pharmacie/', views.historique_pharmacie, name='historique_pharmacie'),
path('historique_livreur/', views.historique_livreur, name='historique_livreur'),
path('historique_patient', views.historique_patient, name='historique_patient'),

path('recherche-produit/' , views.recherche_produit , name='recherche-produit'),

path('envoyer_commande/', views.envoyer_commande, name='envoyer_commande'),
path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
path('accepter_commande/<int:commande_id>/', views.accepter_commande, name='accepter_commande'),
path('product/<int:id_produit>/delete/', ProductDeleteView.as_view(), name='product-delete'),
path('accepter_commande_liv/<int:commande_id>/', views.accepter_commande_liv, name='accepter_commande_liv'),
path('refuser_commande/<int:commande_id>/', views.refuser_commande, name='refuser_commande'),

path('admin2/' , views.admin2 , name='admin2'),
path('medecin/' , views.medecin , name='medecin'),
path('pharmacie/' , views.pharmacie , name='pharmacie'),
path('patient/' , views.patient, name='patient'),
path('pharmacie_details/<int:user_id>/', views.pharmacie_details, name='pharmacie_details'),
path('commandes-pharmacie/', views.commandes_pharmacie, name='commandes-pharmacie'),
path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

path('footer', views.footer, name='footer'),
path('confirmationpharm/', views.confirmationpharm, name='confirmationpharm'),
path('checkoutout/', views.checkoutout, name='checkoutout'),
path('medecin_details/<int:user_id>/', views.medecin_details, name='medecin_details'),
path('ajouter_produit/', views.ajouter_produit, name='ajouter_produit'),



]