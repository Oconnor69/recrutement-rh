# forms.py
from django import forms
from .models import RH

class RHForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = RH
        fields = ['nom', 'prenom', 'matricule', 'email', 'mot_de_passe','status']

    def save(self, commit=True):
        rh = super().save(commit=False)
        rh.set_mot_de_passe(self.cleaned_data["mot_de_passe"])
        if commit:
            rh.save()
        return rh


class RHLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# forms.py
from django import forms
from .models import Offre

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        exclude = ['date_publication','rh']  # auto-set
        widgets = {
            'date_expiration': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import Candidat
from django import forms
from .models import Candidat

class CandidatRegisterForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirmer_mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = Candidat
        fields = [
            'nom', 'prenom', 'email', 'mot_de_passe', 'confirmer_mot_de_passe',
            'date_naissance', 'sexe', 'telephone', 'adresse', 'ville', 'pays',
            'titre_profil', 'resume_professionnel', 'linkedin_url', 'github_url',
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'resume_professionnel': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get('mot_de_passe')
        confirmer = cleaned_data.get('confirmer_mot_de_passe')
        if mot_de_passe and confirmer and mot_de_passe != confirmer:
            self.add_error('confirmer_mot_de_passe', "Les mots de passe ne correspondent pas.")
        return cleaned_data


class CandidatLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")


# forms.py
from django import forms
from .models import Candidature

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        exclude = ['candidat', 'offre', 'date_postulation', 'statut']
        widgets = {
            'lettre_de_motivation': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
            'cv': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
            'cin': forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png'}),
            'diplome': forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png'}),
        }

# forms.py
from django import forms
from .models import Candidat

class CandidatForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Candidat
        exclude = ['mot_de_passe']  # mot_de_passe géré à part

    def save(self, commit=True):
        candidat = super().save(commit=False)
        mot_de_passe = self.cleaned_data.get('mot_de_passe')
        if mot_de_passe:
            candidat.set_mot_de_passe(mot_de_passe)
        if commit:
            candidat.save()
        return candidat
