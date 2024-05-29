from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField('Is_admin' , default=False)
    is_medecin= models.BooleanField('Is medecin' , default=False)
    is_pharmacie= models.BooleanField('Is pharmacie' , default=False)
    is_patient= models.BooleanField('Is patient' , default=False)
    is_livreur= models.BooleanField('Is livreur' , default=False)


class Admin2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , default=2)
    nom_Admin = models.CharField(max_length=255 , default="Admin")
    password = models.CharField(max_length=255, blank=True, null=True)
class Livreur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , default=2)

    nom_liv = models.CharField(max_length=100)
    num_tel = models.CharField(max_length=15)
    adresse_liv = models.CharField(max_length=200)
    disponible = models.BooleanField(default=False)
    ville = models.CharField(max_length=100 , default="Alger" )



    def __str__(self):
        return self.nom_liv
    def marquer_disponible(self):
        self.disponible = True
        self.save()

    def marquer_non_disponible(self):
        self.disponible = False
        self.save() 
class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_medecin = models.CharField(max_length=255 , default="Medecin Anonyme")
    adresse_cabinet = models.CharField(max_length=255, blank=True, null=True)
    heure_ouverture = models.TimeField(blank=True, null=True)
    heure_fermeture = models.TimeField(blank=True, null=True)
    jours_travail = models.CharField(max_length=255, blank=True, null=True)
    specialite = models.CharField(max_length=255, blank=True, null=True)
    num_tel = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)

class Produit(models.Model):
    id_produit = models.AutoField(primary_key=True)
    nom_pr = models.CharField(max_length=100)
    Description = models.CharField(max_length=10000 , null=True)

    prix_unitaire = models.DecimalField(
        max_digits=10, decimal_places=2, default=None , null=True)
    
    image = models.CharField( max_length=2000   , default=None, null=True)

    TYPE_CHOICES = [
        ('Pharmaceutique', 'Produit Pharmaceutique'),
        ('Medicament', 'Médicament'),
    ]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    Qte = models.CharField(max_length=100, blank=True, null=True)

    # Attributs spécifiques aux produits pharmaceutiques
    dosage = models.CharField(max_length=100, blank=True, null=True)
    ordonnance_requise = models.BooleanField(default=False , null=True)



    def __str__(self):
        return self.nom_pr

class Pharmacie(models.Model):
    

    user = models.OneToOneField(User, on_delete=models.CASCADE , primary_key=True)

    nom = models.CharField(max_length=255)
    heure_ouverturep = models.TimeField(blank=True, null=True)
    heure_fermeturep = models.TimeField(blank=True, null=True)
    nom_responsable = models.CharField(max_length=255, blank=True, null=True)
    num_tel = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    produits = models.ManyToManyField(Produit)
    def __str__(self):
        return self.nom
    def __str__(self):
        return f"Pharmacie: {self.nom}, Responsable: {self.nom_responsable}, Numéro de téléphone: {self.num_tel}, Adresse: {self.adresse}"


class Produit_Prescris(models.Model):
    id_produitprescris = models.AutoField(primary_key=True)
    nom_prp = models.CharField(max_length=100)
    Descriptionp= models.CharField(max_length=10000 , null=True)

class Commande(models.Model):
    id_commande = models.AutoField(primary_key=True)
    nom_utilisateur = models.CharField(max_length=100 , default=None)
    total = models.CharField(max_length=200 , default=None)
    date_commande = models.DateTimeField(auto_now=True)
    ville = models.CharField(max_length=100 )
    adr_mail = models.CharField(max_length=100 , default=None)
    adresse =  models.CharField(max_length=100 , default=None)
    num_tel = models.CharField(max_length=15, null=True)
    pharmacie = models.ForeignKey(Pharmacie, on_delete=models.CASCADE, related_name="commandes")

    items = models.CharField(max_length=300 , default=None)
   
    class Meta:
        ordering = ['-date_commande']
    def __str__(self):
        return self.nom_utilisateur 

   
class Produit_Prescris(Produit):
    id_produitprescris = models.AutoField(primary_key=True)
    nom_prp = models.CharField(max_length=100)
    Descriptionp= models.CharField(max_length=10000 , null=True)




class PharmaCommandes(models.Model):
    id_commandepharm = models.AutoField(primary_key=True)
    nom_utilisateur = models.CharField(max_length=100 , default=None)
    prenom_utilisateur = models.CharField(max_length=100 , default=None)
    total = models.CharField(max_length=200 , default=None)
    date_commande = models.DateTimeField(auto_now=True)
    ville = models.CharField(max_length=100 )
    adr_mail = models.CharField(max_length=100 , default=None)
    adresse =  models.CharField(max_length=100 , default=None)
    num_tel = models.CharField(max_length=15, null=True)

    items = models.CharField(max_length=300 , default=None)
    ordonnance = models.FileField(upload_to='ordonnances/', null=True, blank=True)  # Le paramètre 'upload_to' spécifie où stocker les fichiers
    pharmacie = models.ForeignKey(Pharmacie, on_delete=models.CASCADE , default=12)
    livreur = models.ForeignKey(Livreur, on_delete=models.SET_NULL, null=True, blank=True)
    ETAT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTE', 'Accepté'),
        ('EN_COURS_DE_LIVRAISON', 'En cours de livraison'),
        ('ACCEPTEE PAR LE LIVREUR ', 'Accéptée par le livreur'),
        ('REFUSEE PAR LE LIVREUR', 'Refusée par le livreur'),
        ('LIVRE', 'Livré'), 
    ]

    # Champ pour l'état de la commande
    etat = models.CharField(max_length=200, choices=ETAT_CHOICES, default='EN_ATTENTE')

    class Meta:
        ordering = ['-date_commande']
    def __str__(self):
        return self.nom_utilisateur 
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_patient = models.CharField(max_length=255)
    sexe = models.CharField(max_length=1, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    num_tel = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    commandes = models.ManyToManyField(PharmaCommandes)

class InfosPatient(models.Model):
    id_infos_patient = models.AutoField(primary_key=True  )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    nom = models.CharField(max_length=100)
    age = models.IntegerField()
    sexe = models.CharField(max_length=10 , null=True  )

class Ordonnance(models.Model):
    id_ordonnance = models.AutoField(primary_key=True, default=None)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE , default='' )
    infos_patient = models.ForeignKey(InfosPatient, on_delete=models.CASCADE , default='1'  )
    produits = models.ManyToManyField(Produit_Prescris)
    date_creation = models.DateTimeField(default=timezone.now)  # Utilisez timezone.now pour enregistrer la date actuelle lors de la création

    def save(self, *args, **kwargs):
        # Assurez-vous que la date de création est mise à jour uniquement lors de la création de l'objet
        if not self.id_ordonnance:
            self.date_creation = timezone.now()
        super().save(*args, **kwargs)
    
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    nom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Messagerie(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'
