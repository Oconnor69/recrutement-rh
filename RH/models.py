# models.py

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


class RH(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    matricule = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=191, unique=True)
    mot_de_passe = models.CharField(max_length=128)
    STATUS_CHOICES = (
        (0, "Employé"),   # ou “Viewer”, “Standard”… à toi de choisir
        (1, "Administrateur"),
    )

    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=0,
        help_text="0 = employé, 1 = admin"
    )
    entreprise_nom = models.CharField(
        max_length=100,
        default="ONEE",
        editable=False
    )

    def set_mot_de_passe(self, raw_password):
        self.mot_de_passe = make_password(raw_password)

    def check_mot_de_passe(self, raw_password):
        return check_password(raw_password, self.mot_de_passe)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"


class Offre(models.Model):
    titre = models.CharField(max_length=100)
    rh = models.ForeignKey(RH, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    categorie = models.CharField(
        max_length=50,
        choices=[
            ('INFORMATIQUE', 'Informatique'),
            ('MARKETING', 'Marketing'),
            ('RESSOURCES_HUMAINES', 'Ressources Humaines'),
            ('FINANCE', 'Finance'),
            ('AUTRE', 'Autre'),
        ],
        default='AUTRE'
    )
    exigences = models.TextField(blank=True, null=True)
    salaire = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_contrat = models.CharField(
        max_length=50,
        choices=[
            ('CDI', 'CDI'),
            ('CDD', 'CDD'),
            ('Stage', 'Stage'),
            ('Freelance', 'Freelance'),
            ('Alternance', 'Alternance'),
        ],
        blank=True,
        null=True
    )
    localisation = models.CharField(max_length=100, blank=True, null=True)
    date_publication = models.DateField(auto_now_add=True)
    date_expiration = models.DateField()
    experience_requise = models.CharField(max_length=100, blank=True, null=True)
    nombre_postes = models.PositiveIntegerField(
        default=1,
        help_text="Nombre de postes disponibles pour cette offre"
    )
    niveau_etude = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ex : Bac+3, Bac+5, Master, Doctorat, etc."
    )
    @property
    def is_active(self):
        return self.date_expiration >= timezone.now().date()
    def __str__(self):
        return self.titre


class Candidat(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=191, unique=True)
    mot_de_passe = models.CharField(max_length=128, default="default")
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(
        max_length=10,
        choices=[
            ('HOMME', 'Homme'),
            ('FEMME', 'Femme'),
            ('AUTRE', 'Autre'),
        ],
        default='AUTRE'
    )
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True, default="Maroc")
    titre_profil = models.CharField(max_length=100, blank=True, null=True, help_text="Titre résumant le profil professionnel")
    resume_professionnel = models.TextField(blank=True, null=True, help_text="Un court résumé de votre parcours et de vos objectifs")
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)
    def __str__(self):
        return f"{self.candidat} → {self.offre}"

    def save(self, *args, **kwargs):
        # Detect if status is changing
        if self.pk:
            old = Candidature.objects.get(pk=self.pk)
            if old.statut != self.statut and self.statut in ['concours_Ecrit', 'concours_Oral']:
                self.envoyer_convocation()

        super().save(*args, **kwargs)

    def envoyer_convocation(self):
        sujet = f"Convocation au {self.get_statut_display()}"
        message = (
            f"Bonjour {self.candidat.prenom},\n\n"
            f"Vous êtes convoqué(e) pour le {self.get_statut_display().lower()} concernant le poste : {self.offre.titre}.\n"
            f"Veuillez consulter votre espace candidat pour plus d’informations.\n\n"
            f"Cordialement,\nL’équipe RH de {self.offre.rh.entreprise_nom if self.offre.rh else 'l\'entreprise'}"
        )
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.candidat.email],
            fail_silently=False,
        )
    def set_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe = make_password(mot_de_passe)

    def check_mot_de_passe(self, mot_de_passe):
        return check_password(mot_de_passe, self.mot_de_passe)

    def is_authenticated(self):
        return True

    class Meta:
        verbose_name = "Candidat"
        verbose_name_plural = "Candidats"

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Candidature(models.Model):
    STATUTS = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTEE', 'Acceptée'),
        ('concours_Ecrit', 'Concours écrit'),
        ('concours_Oral', 'Concours oral'),
        ('REFUSEE', 'Refusée'),
    ]
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date_postulation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_ATTENTE')
    niveau_etude = models.CharField(
        max_length=100,
        choices=[
            ('BAC', 'Baccalauréat'),
            ('BAC+2', 'Bac +2'),
            ('BAC+3', 'Bac +3'),
            ('BAC+5', 'Bac +5'),
            ('DOCTORAT', 'Doctorat'),
            ('AUTRE', 'Autre'),
        ],
        default='BAC'
    )
    annee_experience = models.PositiveIntegerField(default=0)
    lettre_de_motivation = models.FileField(upload_to='motivation/', blank=True, null=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    cin = models.FileField(upload_to='cin/', blank=True, null=True)
    diplome = models.FileField(upload_to='diplome/', blank=True, null=True)
    permis = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.candidat} → {self.offre}"
