from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Votre adresse email",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full", "placeholder": "Prénom"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full", "placeholder": "Nom"}
        ),
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style password fields
        self.fields["password1"].widget.attrs.update(
            {"class": "input input-bordered w-full", "placeholder": "Mot de passe"}
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "placeholder": "Confirmer le mot de passe",
            }
        )

    def clean_email(self):
        """
        S'assurer que l'email est unique.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Un compte avec cette adresse email existe déjà."
            )
        return email

    def save(self, commit=True):
        """
        Sauvegarde l'utilisateur avec un nom d'utilisateur généré automatiquement.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        # Générer le nom d'utilisateur au format Nom.Prenom
        first_name = self.cleaned_data["first_name"].strip()
        last_name = self.cleaned_data["last_name"].strip()

        # Nettoyer les noms (enlever les espaces, caractères spéciaux)
        first_name_clean = "".join(c for c in first_name if c.isalnum())
        last_name_clean = "".join(c for c in last_name if c.isalnum())

        # Créer le nom d'utilisateur de base
        base_username = f"{last_name_clean}.{first_name_clean}".lower()

        # Vérifier si le nom d'utilisateur existe déjà
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user.username = username

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """
    Formulaire de connexion personnalisé.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Votre adresse email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Mot de passe",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # Supprimer 'request' des kwargs s'il est présent
        kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
