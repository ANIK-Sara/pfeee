from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Produit ,Messagerie , Produit_Prescris
# Create your views here.
from django.http import HttpResponse
from .forms import ProduitForm
from django.contrib.auth.forms import UserChangeForm 
from .forms import CustomPharmacieChangeForm , CustomMedecinChangeForm
from .forms import CustomLivreurChangeForm
from .forms import CustomPatientChangeForm
from .forms import CustomAdminChangeForm
from django.db.models import Count
from django.http import Http404
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render , redirect 
from .forms import SignUpForm , LoginForm
from django.contrib.auth import authenticate , login
from . models import Medecin , Patient , Pharmacie  , Produit  , Admin2
from django.shortcuts import render, redirect , get_object_or_404
from django.core.exceptions import ValidationError
from .models import  Medecin, Patient, Pharmacie , Produit , Ordonnance , Commande  , Livreur
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.http import JsonResponse
from .models import Pharmacie
from django.core.paginator import Paginator 
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import auth 

from django.contrib.auth.hashers import make_password
from django.contrib import messages
logger = logging.getLogger(__name__)

import json
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import  Patient, Medecin, Pharmacie , PharmaCommandes
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import  Contact 
from django.http import HttpResponse
from .models import InfosPatient, Ordonnance, Patient, Medecin, Produit
from .models import Messagerie  # Assurez-vous d'importer le modèle Message


def page_de_garde(request):
    return render(request, 'app1/pagegarde.html')

def a_propos(request):
    return render(request, 'apropos.html')




def messagerie_medecin(request):
    
    return render(request, 'app1/messagerie_medecin.html')


def messagerie_pharmacie(request):
    query = request.GET.get('q')
    print("salut")
    if query:
        print("salut")
        medecins = Medecin.objects.filter(nom_medecin__icontains=query)
    else:
        print("salut")
        medecins = Medecin.objects.all()
    
    return render(request, 'app1/messagerie_pharmacie.html', {'medecins': medecins})

def messages_recus(request):
    # Ajoutez la logique pour les messages reçus
    pass



def envoyer_message(request, medecin_id):
    # Ajoutez la logique pour envoyer un message
    pass

def creer_ordonnance(request):
    if request.method == 'POST':
        medecin_user = request.POST.get('medecin_user')
        patient_user = request.POST.get('patient_user')
        nom_patient = request.POST.get('nom_patient')
        age_patient = request.POST.get('age_patient')
        sexe_patient = request.POST.get('sexe_patient')

        produits = request.POST.getlist('produit[]')
        descriptions = request.POST.getlist('description[]')

        if not sexe_patient:
            return HttpResponse("Veuillez sélectionner le sexe du patient.")

        try:
            medecin_user_obj = User.objects.get(username=medecin_user, is_medecin=True)
            medecin = Medecin.objects.get(user=medecin_user_obj)
        except User.DoesNotExist:
            return HttpResponse("Médecin non trouvé", status=404)
        except Medecin.DoesNotExist:
            return HttpResponse("Médecin non trouvé", status=404)

        try:
            patient_user_obj = User.objects.get(username=patient_user, is_patient=True)
            patient = Patient.objects.get(user=patient_user_obj)
        except User.DoesNotExist:
            return HttpResponse("Patient non trouvé", status=404)
        except Patient.DoesNotExist:
            return HttpResponse("Patient non trouvé", status=404)

        infos_patient = InfosPatient.objects.create(
    patient=patient,
    nom=nom_patient,
    age=age_patient,
    sexe=sexe_patient
)

        # Créer l'ordonnance sans produits
        ord = Ordonnance.objects.create(
            medecin=medecin,
            infos_patient=infos_patient,
            date_creation=timezone.now() 
        )

        # Ajouter les produits prescrits à l'ordonnance
        for produit, description in zip(produits, descriptions):
            if produit:
                produit_prescris = Produit_Prescris.objects.create(
                    nom_prp=produit,
                    Descriptionp=description
                )
                ord.produits.add(produit_prescris)

        # Sauvegarder les modifications de l'ordonnance après avoir ajouté les produits
        ord.save()

        return redirect('creer_ordonnance')  # Rediriger vers une page de confirmation

    else:
        medecin = get_medecin_from_request(request)
        return render(request, 'app1/medecin.html', {'medecin': medecin})

def get_medecin_from_request(request):
    user = request.user
    try:
        return Medecin.objects.get(user=user)
    except Medecin.DoesNotExist:
        return None

def get_patient_from_request(request):
    user = request.user
    try:
        return Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        return None

def search_patient(request):
    query = request.GET.get('q')
    print(1)
    if query:
        print(2)
    
        patients = Patient.objects.filter(nom_patient__icontains=query)
    else:
        print(3)
        patients = Patient.objects.all()# Aucun résultat si aucun paramètre de recherche n'est fourni
    return render(request, 'app1/medecin.html', {'patients': patients})



def historique_medecin(request):
    medecin = request.user.medecin  # Supposons que vous ayez une relation OneToOne entre User et Medecin
    ordonnances = Ordonnance.objects.filter(medecin=medecin)
    patients = set(ordo.infos_patient for ordo in ordonnances)
    
    context = {
        'medecin': medecin,
        'ordonnances': ordonnances,
        'patients': patients
    }
    return render(request, 'app1/historique_medecin.html', context)


def patient_ordonnances(request):
    # Récupérer l'utilisateur connecté
    user = request.user
    
    # Récupérer l'instance de Patient associée à l'utilisateur connecté
    patient = Patient.objects.get(user=user)
    
    # Récupérer tous les objets InfosPatient associés au patient
    infos_patients = InfosPatient.objects.filter(patient=patient)
    
    # Récupérer toutes les ordonnances associées à chaque objet InfosPatient
    ordonnances = []
    for infos_patient in infos_patients:
        ordonnances.extend(infos_patient.ordonnance_set.all())
    
    return render(request, 'app1/patient_ordonnances.html', {'patient': patient, 'ordonnances': ordonnances})





@login_required
def envoyer_message(request):
    if request.method == 'POST':
        medecin_user = request.POST.get('medecin_user')
        message = request.POST.get('message')
        
        if not medecin_user:
            raise Http404("Le nom d'utilisateur du médecin est manquant.")

        try:
            medecin = User.objects.get(username=medecin_user, is_medecin=True)
        except User.DoesNotExist:
            raise Http404("Aucun médecin ne correspond à ce nom d'utilisateur.")
        
        Messagerie.objects.create(
            sender=request.user,  # La pharmacie est le sender
            receiver=medecin,     # Le médecin est le receiver
            message=message
        )
        return redirect('messagerie_pharmacie')
    
    return redirect('messagerie_pharmacie')
@login_required
def messages_recus(request):
    messages = Messagerie.objects.filter(receiver=request.user).order_by('-timestamp')

    return render(request, 'app1/messages_recus.html', {'messages': messages})
def messages_recus_pharmacie(request):
    messages = Messagerie.objects.filter(receiver=request.user).order_by('-timestamp')

    return render(request, 'app1/messages_recus_pharmacie.html', {'messages': messages})
@login_required
def repondre_message(request):
    if request.method == 'POST':
        pharmacie_id = request.POST.get('pharmacie_id')
        message = request.POST.get('message')
        pharmacie = User.objects.filter(id=pharmacie_id, is_pharmacie=True).first()
        if pharmacie:
            Messagerie.objects.create(
                sender=request.user,  # Le médecin est le sender
                receiver=pharmacie,   # La pharmacie est le receiver
                message=message
            )
            return redirect('messagerie_medecin')
        else:
            # Gérer le cas où aucune pharmacie ne correspond à l'ID donné
            raise Http404("Aucune pharmacie ne correspond à cet ID.")
    # Si la méthode n'est pas POST, rediriger l'utilisateur vers la page appropriée
    return redirect('messagerie_medecin')


@login_required
def repondre_message_medecin(request, pharmacie_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        receiver = User.objects.filter(is_pharmacie=pharmacie_id).first()
        if receiver:
            Messagerie.objects.create(
                sender=request.user,
                receiver=receiver,
                message=message
            )
            return redirect('messagerie_medecin')
        else:
            # Gérer le cas où aucune pharmacie ne correspond à l'ID donné
            raise Http404("Aucune pharmacie correspond à cet ID.")
    return render(request, 'app1/messages_recus.html', {'pharmacie_id': pharmacie_id})

def messages_envoyes(request):
    messages_envoyes = Messagerie.objects.filter(sender=request.user)
    return render(request, 'app1/messages_envoyes.html', {'messages_envoyes': messages_envoyes})

def get_message_details(request):
    try:
        message_id = request.GET.get('message_id')
        if not message_id:
            return JsonResponse({'error': 'message_id is required'}, status=400)
        
        message = get_object_or_404(Messagerie, id=message_id)
        data = {
            'sender': message.sender.username,
            'date': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'content': message.message
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def contactez_nous(request):
    if request.method == 'POST':
        # Assurez-vous que l'utilisateur est connecté
        if not request.user.is_authenticated:
            return redirect('login')  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté

        nom = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        role = request.POST.get('role')

        # Créer une nouvelle instance du modèle Contact et enregistrer les données
        Contact.objects.create(user=request.user, nom=nom, email=email, message=message, role=role)
        
        # Redirection vers une page de confirmation ou autre
        return redirect('confirmation_contact')
    else:
        return render(request, 'app1/contactez_nous.html')

    return render(request, 'app1/contactez_nous.html')

def confirmation_contact(request):
    
    return render(request, 'app1/confirmation_contact.html')

def messages_contact(request):
    messages = Contact.objects.all()
    return render(request, 'app1/messages_contact.html', {'messages': messages})



def livraison_terminee(request):
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        
        # Récupérer la commande
        commande = get_object_or_404(PharmaCommandes, id_commandepharm=commande_id)
        
        # Mettre à jour l'état de la commande
        commande.etat = 'livré'
        commande.save()
        
        # Rediriger l'utilisateur vers la page du livreur
        return HttpResponseRedirect(reverse('livreur'))

    # Si la requête n'est pas de type POST, rediriger vers une page d'erreur ou une autre vue
    return HttpResponseRedirect(reverse('page_d_erreur'))

def accepter_commande(request, commande_id):
    # Récupérer la commande
    commande = PharmaCommandes.objects.get(id_commandepharm=commande_id)

    # Mettre à jour l'état de la commande
    commande.etat = 'Acceptée'
    commande.save()

    # Rediriger vers la page des détails de la commande
    return redirect('commande_details', commande_id=commande_id)

def accepter_commande_liv(request, commande_id):
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        
        # Récupérer la commande
        commande = get_object_or_404(PharmaCommandes, id_commandepharm=commande_id)
        
        # Mettre à jour l'état de la commande
        commande.etat = 'acceptée par le livreur'
        commande.save()
        
        # Rediriger l'utilisateur vers la page du livreur
        return HttpResponseRedirect(reverse('livreur'))

    # Si la requête n'est pas de type POST, rediriger vers une page d'erreur ou une autre vue
    return HttpResponseRedirect(reverse('page_d_erreur'))

def refuser_commande(request, commande_id):
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        
        # Récupérer la commande
        commande = get_object_or_404(PharmaCommandes, id_commandepharm=commande_id)
        
        # Mettre à jour l'état de la commande et dissocier le livreur
        commande.etat = 'refusé par le livreur'
        commande.livreur = None  # Dissocier le livreur de la commande
        commande.save()
        
        # Rediriger l'utilisateur vers la page du livreur
        return HttpResponseRedirect(reverse('livreur'))

    # Si la requête n'est pas de type POST, rediriger vers une page d'erreur ou une autre vue
    return HttpResponseRedirect(reverse('page_d_erreur'))
@login_required
def mes_commandes(request):
    # Récupérer le patient connecté
    patient = request.user.patient  # Supposons que le modèle User est étendu avec un modèle Patient

    # Récupérer les commandes associées au patient
    commandes = patient.commandes.all()

    # Remplacer les états "acceptée par le livreur" et "refusée par le livreur" par "en cours de livraison"
    for commande in commandes:
        if commande.etat in ["acceptée par le livreur", "refusé par le livreur"]:
            commande.etat_affiche = "en cours de livraison"
        else:
            commande.etat_affiche = commande.etat

    return render(request, 'app1/commandes_patient.html', {'commandes': commandes})
def envoyer_commande(request):
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        livreur_nom = request.POST.get('livreur_nom')
        
        # Récupérer la commande et le livreur
        commande = get_object_or_404(PharmaCommandes, id_commandepharm=commande_id)
        livreur = get_object_or_404(Livreur, nom_liv=livreur_nom)
        
        # Associer le livreur à la commande
        commande.livreur = livreur
        commande.etat = 'en_cours_de_livraison'  # Mettre à jour l'état de la commande
        commande.save()
        
        # Rediriger l'utilisateur vers une page de confirmation
        return redirect('commande_details', commande_id=commande_id)
    
    return redirect('commande_details') 


def commande_details(request, commande_id):
    # Récupérer la commande en fonction de l'identifiant
    commande = PharmaCommandes.objects.get(id_commandepharm=commande_id)
    
    # Filtrer les livreurs en fonction de leur ville
    livreurs = Livreur.objects.filter(ville=commande.ville)
    
    # Passer la commande et les livreurs filtrés à la template pour l'affichage
    return render(request, 'app1/commande_details.html', {'commande': commande, 'livreurs': livreurs})

def commande_details_liv(request, commande_id):
    # Récupérer la commande en fonction de l'identifiant
    commande = PharmaCommandes.objects.get(id_commandepharm=commande_id)
    return render(request, 'app1/commande_details_liv.html', {'commande': commande})



def ajouter_produit(request):
    if request.method == 'POST':
        nom_pr = request.POST.get('nom_pr')
        description = request.POST.get('description')
        prix_unitaire = request.POST.get('prix_unitaire')
        image = request.POST.get('image')
        type_produit = request.POST.get('type')
        dosage = request.POST.get('dosage')
        ordonnance_requise = request.POST.get('ordonnance_requise')
        Qte = request.POST.get('Qte')
        
        # Créez un nouveau produit
        nouveau_produit = Produit.objects.create(
            nom_pr=nom_pr,
            Description=description,
            prix_unitaire=prix_unitaire,
            image=image,
            type=type_produit,
            dosage=dosage,
            ordonnance_requise=ordonnance_requise,
            Qte=Qte
        )
        
        # Récupérez la pharmacie de l'utilisateur connecté
        pharmacie = Pharmacie.objects.get(user=request.user)
        
        # Ajoutez le nouveau produit à la pharmacie
        pharmacie.produits.add(nouveau_produit)
        
        # Redirigez l'utilisateur vers une page de confirmation ou une autre page pertinente
        return redirect('pharmacie')
    else:
        # Gérez le cas où la méthode de requête n'est pas POST
        pass
def index(request):
    return render(request , 'app1/index.html')

def register(request):
    msg = None
   
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user = form.save(commit=False)
            user.num_tel = form.cleaned_data['num_tel']
            user.adresse = form.cleaned_data['adresse']
            user.save()
            if user.is_admin:
                user.save()
                Admin2.objects.create(user=user , nom_Admin=user.username )
            elif user.is_medecin:
                user.save()
                Medecin.objects.create(user=user , nom_medecin=user.username ,
                  
                    num_tel=user.num_tel,
                    adresse=user.adresse,  
                    adresse_cabinet=form.cleaned_data.get('adresse_cabinet', ''),
                    heure_ouverture=form.cleaned_data.get('heure_ouverture', None),
                    heure_fermeture=form.cleaned_data.get('heure_fermeture', None),
                    jours_travail=form.cleaned_data.get('jours_travail', ''),
                    specialite=form.cleaned_data.get('specialite', ''))
            elif user.is_livreur:
                user.save()
                Livreur.objects.create(user=user , nom_liv =user.username ,num_tel=user.num_tel , 
                                       adresse_liv = user.adresse ,
                                       disponible=form.cleaned_data.get('disponible', ''),
                                       ville=form.cleaned_data.get('ville', ''),)
            elif user.is_pharmacie:
                user.save()
                Pharmacie.objects.create(user=user ,  num_tel=user.num_tel,
                    adresse=user.adresse, nom =user.username,heure_ouverturep=form.cleaned_data.get('heure_ouverturep', None),
                    heure_fermeturep=form.cleaned_data.get('heure_fermeturep', None),
                    nom_responsable=form.cleaned_data.get('nom_responsablep', ''))
                
            elif user.is_patient:
                user.save()
                Patient.objects.create(user=user , num_tel=user.num_tel,
                    adresse=user.adresse, nom_patient=user.username,
                                        sexe=form.cleaned_data.get('sexe', ''),
                    date_naissance=form.cleaned_data.get('date_naissance', None))
            msg = 'user created'
            return redirect('login_view')
        else:
            print("Form is not valid:", form.errors)
            msg = 'form is not valid '
    else:
        form = SignUpForm()
    return render(request , 'app1/register.html' , {'form': form , 'msg' : msg })


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username , password=password)
            if user is not None and user.is_admin:
                login(request , user) 
                return redirect ('admin2')
            elif  user is not None and user.is_medecin:
                login(request , user) 
                return redirect ('medecin')
            elif  user is not None and user.is_livreur:
                login(request , user) 
                return redirect ('livreur')
            elif user is not None and user.is_pharmacie:
                login(request , user) 
                return redirect ('pharmacie')
            elif user is not None and user.is_patient:
                login(request , user) 
                return redirect ('patient')
            else:
                msg = 'invalid credentials'
        else: 
            msg = 'error validation form'
    return render (request , 'app1/login.html' , {'form': form  , 'msg' : msg})

def deconnexion(request):
    # Logique de déconnexion de l'utilisateur
    # Par exemple, supprimer la session de l'utilisateur
    # Rediriger l'utilisateur vers une page de connexion ou une autre page appropriée
    return redirect('login_view') 


def profile(request):
    pharmacie_instance = request.user.pharmacie
    if request.method == 'POST':
        form = CustomPharmacieChangeForm(request.POST, instance=pharmacie_instance)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomPharmacieChangeForm(instance=pharmacie_instance)
    return render(request, 'app1/profil.html', {'form': form})


def profileliv(request):
    livreur_instance = request.user.livreur
    if request.method == 'POST':
        form = CustomLivreurChangeForm(request.POST, instance=livreur_instance)
        if form.is_valid():
            form.save()
            return redirect('profileliv')
    else:
        form = CustomLivreurChangeForm(instance=livreur_instance)
    return render(request, 'app1/profilliv.html', {'form': form})

def profilmed(request):
    medecin_instance = request.user.medecin
    if request.method == 'POST':
        form = CustomMedecinChangeForm(request.POST, instance=medecin_instance)
        if form.is_valid():
            form.save()
            return redirect('profilmed')
    else:
        form = CustomMedecinChangeForm(instance=medecin_instance)
    return render(request, 'app1/profilmed.html', {'form': form})

def profileadmin(request):
    admin_instance = request.user.admin2
    if request.method == 'POST':
        form = CustomAdminChangeForm(request.POST, instance=admin_instance)
        if form.is_valid():
            form.save()
            return redirect('profileadmin')
    else:
        form = CustomAdminChangeForm(instance=admin_instance)
    return render(request, 'app1/profileadmin.html', {'form': form})

def profilepatient(request):
    patient_instance = request.user.patient
    if request.method == 'POST':
        form = CustomPatientChangeForm(request.POST, instance=patient_instance)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomPatientChangeForm(instance=patient_instance)
    return render(request, 'app1/profilepatient.html', {'form': form})

def livreur(request):
    # Récupérer l'utilisateur actuel
    user = request.user

    # Récupérer le livreur associé à l'utilisateur actuel
    livreur = get_object_or_404(Livreur, user=user)

    # Récupérer toutes les commandes associées à ce livreur
    commandes = PharmaCommandes.objects.filter(livreur=livreur).exclude(etat="livré")

    return render(request, 'app1/livreur.html', {'commandes': commandes, 'livreur': livreur})
User = get_user_model()
def admin2(request):
    query = request.GET.get('search')
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    else:
        users = User.objects.all()

    # Calcul des pourcentages par rôle
    total_users = users.exclude(is_admin=True).count()
    roles_count = users.exclude(is_admin=True).values('is_medecin', 'is_pharmacie', 'is_patient', 'is_livreur').annotate(count=Count('id'))
    roles_data = {
        'Medecin': 0,
        'Pharmacie': 0,
        'Patient': 0,
        'Livreur': 0
    }
    for role in roles_count:
        if role['is_medecin']:
            roles_data['Medecin'] = role['count']
        elif role['is_pharmacie']:
            roles_data['Pharmacie'] = role['count']
        elif role['is_patient']:
            roles_data['Patient'] = role['count']
        elif role['is_livreur']:
            roles_data['Livreur'] = role['count']

    roles_percentage = {k: (v / total_users) * 100 for k, v in roles_data.items()}

    return render(request, 'app1/admin.html', {
        'users': users,
        'roles_percentage': roles_percentage
    })


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_password = request.POST.get('password')
        if new_password:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, f'Le mot de passe de {user.username} a été mis à jour.')
            return redirect('admin2')

    return render(request, 'app1/edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, f"L'utilisateur {user.username} a été supprimé.")
    return redirect('admin2')

def medecin(request):
   
    return render(request , 'app1/medecin.html')


def pharmacie(request):
    user = request.user
    pharmacie = get_object_or_404(Pharmacie, user=user)
    product_objectt = pharmacie.produits.all()  # Utilisation de la relation avec le modèle de produit
    paginator = Paginator(product_objectt, 8)  # Changer 8 à 6 pour afficher 6 produits par page
    page_number = request.GET.get('page')
    product_object = paginator.get_page(page_number)
    return render(request, 'app1/pharmacie.html', {
        'pharmacie': pharmacie, 
        'product_objectt': product_objectt, 
        'product_object': product_object
    })

def commandes_pharmacie(request):
    user = request.user
    pharmacie = get_object_or_404(Pharmacie, user=user)
    commandes = PharmaCommandes.objects.filter(pharmacie=pharmacie).exclude(etat="livré")

    return render(request, 'app1/commande.html', {'pharmacie': pharmacie, 'commandes': commandes})


def patient(request):
     query = request.GET.get('query', '')

    # Initialisation des résultats
     medecins = Medecin.objects.none()
     pharmacies = Pharmacie.objects.none()
     produits = Produit.objects.none()
     pharmacies_avec_produits = Pharmacie.objects.none() 

    # Rechercher des médecins par nom ou spécialité
     if query:
        medecins = Medecin.objects.filter(nom_medecin__icontains=query )| \
               Medecin.objects.filter(specialite__icontains=query) | \
               Medecin.objects.filter(adresse_cabinet__icontains=query) 
        
        

        # Rechercher des pharmacies par nom ou nom du responsable
        pharmacies = Pharmacie.objects.filter(nom__icontains=query)| \
                 Pharmacie.objects.filter(adresse__icontains=query)
        
        # Rechercher des produits par nom
        produits = Produit.objects.filter(nom_pr__icontains=query)
         # Récupérer les pharmacies associées aux produits trouvés
        if produits.exists():
            pharmacies_avec_produits = Pharmacie.objects.filter(produits__in=produits)

    # Pagination
     paginator = Paginator(medecins, 8)  # 8 résultats par page
     page_number = request.GET.get('page')
     medecin_page = paginator.get_page(page_number) 

     paginator = Paginator(pharmacies, 8)  # 8 résultats par page
     page_number = request.GET.get('page')
     pharmacie_page = paginator.get_page(page_number)

     paginator = Paginator(produits, 8)  # 8 résultats par page
     page_number = request.GET.get('page')
     produit_page = paginator.get_page(page_number)

     paginator = Paginator(pharmacies_avec_produits, 8)
     pharmacies_avec_produits_page = paginator.get_page(request.GET.get('page'))

    # Rendu de la vue avec les résultats paginés
     return render(request, 
        'app1/patient.html', 
        {
            'medecins': medecin_page,
            'pharmacies': pharmacie_page,
            'produits': produit_page,
            'pharmacies_avec_produits': pharmacies_avec_produits_page,

            'query': query,  # Conserver la valeur de recherche pour affichage
        })
     


def pharmacie_details(request , user_id):
    user = request.user  # Récupérer l'utilisateur actuel
    pharmacie = get_object_or_404(Pharmacie,  user__id=user_id)
    product_objectt = pharmacie.produits.all()  # Utilisation de la relation avec le modèle de produit
    
    item_namee = request.GET.get('item-namee')
    print("Valeur de item_namee:", item_namee)  # Afficher la valeur de item_namee
    
    if item_namee and item_namee.strip():  # Vérifie si item_namee n'est pas vide
        product_objectt = product_objectt.filter(nom_pr__icontains=item_namee)
    
    print("Produits filtrés:", product_objectt)  # Afficher les produits filtrés
    
    return render(request, 'app1/pharmacie_details.html', {'pharmacie': pharmacie, 'product_objectt': product_objectt})

def medecin_details(request, user_id):
    # Récupérer l'utilisateur actuel
    user = request.user
    
    # Trouver le médecin associé à cet utilisateur
    medecin = get_object_or_404(Medecin, user__id=user_id)
    
    # Récupérer d'autres informations nécessaires pour la vue
    # Si vous avez besoin de filtrer des informations spécifiques
    # par exemple des patients ou des consultations, vous pouvez
    # les récupérer ici de la même manière que pour les produits
    # dans la vue pharmacie_details.
    
    return render(request, 'app1/medecin_details.html', {'medecin': medecin})


def footer(request):
    return render(request , 'app1/footer.html')

def confirmationpharm (request):
    info = PharmaCommandes.objects.all()[:1]
    for item in info:
        nom = item.nom_utilisateur 
    
    return render (request , 'app1/confirmationphar.html' , {'nameph' : nom })

def get_patient_details(patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        return {
            'nom': patient.nom_patient,
            'sexe': patient.sexe,
            'date_naissance': patient.date_naissance,
            'num_tel': patient.num_tel,
            'adresse': patient.adresse
        }
    except Patient.DoesNotExist:
        return None
@login_required
def checkoutout(request):
    ordonnance_requise = False
    panier = {}

    if request.method == "POST":
        panier_str = request.POST.get('items', '{}')
        panier = json.loads(panier_str)

        for produit in panier.values():
            if len(produit) > 3 and produit[3]:
                ordonnance_requise = True
                break

        if ordonnance_requise and 'ordonnance' not in request.FILES:
            return render(
                request,
                'app3/checkoutout.html',
                {
                    'panier': panier,
                    'ordonnance_requise': ordonnance_requise,
                    'message_erreur': "Une ordonnance est requise mais n'a pas été fournie."
                }
            )

        # Récupérer les champs du formulaire
        nom_utilisateur = request.POST.get('nom')
        prenom_utilisateur = request.POST.get('prenom')
        adr_mail = request.POST.get('email')
        num_tel = request.POST.get('tel')
        adresse = request.POST.get('address')
        ville = request.POST.get('ville')
        total = request.POST.get('total', '0')
        items = request.POST.get('items')
        nom_pharmacie = request.POST.get('nomphar')  # Récupérer le nom de la pharmacie

        # Vous devez trouver la pharmacie associée à ce nom
        pharmacie = get_object_or_404(Pharmacie, nom=nom_pharmacie)

        # Sauvegarder la commande avec la pharmacie associée trouvée
        pharcom = PharmaCommandes(
            nom_utilisateur=nom_utilisateur,
            prenom_utilisateur=prenom_utilisateur,
            total=total,
            adr_mail=adr_mail,
            num_tel=num_tel,
            adresse=adresse,
            ville=ville,
            items=items,
            ordonnance=request.FILES.get('ordonnance', None),
            pharmacie=pharmacie  # Associer la commande à la pharmacie trouvée
        )
        pharcom.save()

        # Obtenez le patient connecté
        user = request.user
        try:
            patient = user.patient  # Essayez de récupérer le profil patient
        except Patient.DoesNotExist:
            # Si le profil patient n'existe pas, créez-le
            patient = Patient(user=user)
            patient.save()

        # Associer la commande au patient
        patient.commandes.add(pharcom)

        return redirect('confirmationpharm')


    return render(
        request,
        'app1/checkoutout.html',
        {
            'panier': panier,
            'ordonnance_requise': ordonnance_requise
        }
    )









class ProductDeleteView(View):
    def post(self, request, id_produit):
        product = Produit.objects.get(pk=id_produit)
        product.delete()
        return redirect('pharmacie')
    
def get_produit(request, produit_id):
    produit = get_object_or_404(Produit, id_produit=produit_id)
    data = {
        'id_produit': produit.id_produit,
        'nom_pr': produit.nom_pr,
        'description': produit.Description,
        'prix_unitaire': produit.prix_unitaire,
        'image': produit.image,
        'type': produit.type,
        'dosage': produit.dosage,
        'ordonnance_requise': produit.ordonnance_requise,
        'Qte': produit.Qte
    }
    return JsonResponse(data)
def modifier_produit(request):
    if request.method == 'POST':
        produit_id = request.POST['id_produit']
        produit = get_object_or_404(Produit, id_produit=produit_id)
        produit.nom_pr = request.POST['nom_pr']
        produit.Description = request.POST['description']
        produit.prix_unitaire = request.POST['prix_unitaire']
        produit.image = request.POST['image']
        produit.type = request.POST['type']
        produit.dosage = request.POST['dosage']
        produit.ordonnance_requise = 'ordonnance_requise' in request.POST
        produit.Qte = request.POST['Qte']
        produit.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def recherche_produit(request):
    if request.method == 'GET':
        # Récupérer le terme de recherche saisi dans le formulaire
        terme_recherche = request.GET.get('item-name', '')

        # Effectuer la recherche des produits correspondants
        produits = Produit.objects.filter(nom_pr__icontains=terme_recherche)

        # Passer les produits trouvés au template
        return render(request, 'app1/pharmacie.html', {'product_object': produits})  # Modifier la clé du contexte 
    
def historique_pharmacie(request):
    # Vérifiez si l'utilisateur a une pharmacie associée
    if hasattr(request.user, 'pharmacie'):
        # Récupérer les commandes de la pharmacie avec un état "livré"
        commandes_livrees = PharmaCommandes.objects.filter(pharmacie=request.user.pharmacie, etat="livré")

        context = {
            'commandes_livrees': commandes_livrees
        }

        return render(request, 'app1/historique_pharmacie.html', context)
    else:
        # Si l'utilisateur n'a pas de pharmacie associée, retournez une erreur ou un message approprié
        return render(request, 'app1/historique_pharmacie.html', {'error': 'Aucune pharmacie associée à cet utilisateur'})
    


def historique_livreur(request):
    # Vérifiez si l'utilisateur a une pharmacie associée
    if hasattr(request.user, 'livreur'):
        # Récupérer les commandes de la pharmacie avec un état "livré"
        commandes_livrees = PharmaCommandes.objects.filter(livreur=request.user.livreur, etat="livré")

        context = {
            'commandes_livrees': commandes_livrees
        }

        return render(request, 'app1/historique_livreur.html', context)
    else:
        # Si l'utilisateur n'a pas de pharmacie associée, retournez une erreur ou un message approprié
        return render(request, 'app1/historique_livreur.html', {'error': 'Aucun livreur associée à cet utilisateur'})
    

def historique_patient(request):
    # Vérifiez si l'utilisateur a une pharmacie associée
    if hasattr(request.user, 'patient'):
        # Récupérer les commandes de la pharmacie avec un état "livré"
        commandes_livrees = PharmaCommandes.objects.filter(patient=request.user.patient, etat="livré")

        context = {
            'commandes_livrees': commandes_livrees
        }

        return render(request, 'app1/historique_patient.html', context)
    else:
        # Si l'utilisateur n'a pas de pharmacie associée, retournez une erreur ou un message approprié
        return render(request, 'app1/historique_patient.html', {'error': 'Aucun patient associée à cet utilisateur'})
    pass