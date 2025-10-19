import secrets
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Créer et retourner un utilisateur normal avec un email et un mot de passe.
        """
        if not email:
            raise ValueError("Le champ Email doit être défini")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Créer et retourner un superutilisateur avec un email et un mot de passe."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_adminpanel", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modèle User
    """

    username = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text="Nom d'utilisateur généré automatiquement (affichage uniquement)",
    )
    email = models.EmailField(unique=True)
    key1 = models.CharField(
        max_length=64,
        blank=True,
        help_text="Clé secrète générée automatiquement à la création de l'utilisateur",
    )
    is_employee = models.BooleanField(
        default=False,
        help_text="Indique si cet utilisateur peut accéder à la fonctionnalité de scan QR",
    )
    is_adminpanel = models.BooleanField(
        default=False,
        help_text="Indique si cet utilisateur peut accéder au panneau d'administration",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "users_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"

    def get_full_name(self):
        """
        Retourne le prénom plus le nom, avec un espace entre les deux.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()


@receiver(post_save, sender=User)
def generate_key1(sender, instance, created, **kwargs):
    """
    Gestionnaire de signal pour générer key1 lors de la création d'un nouvel utilisateur.
    """
    if created and not instance.key1:
        instance.key1 = secrets.token_urlsafe(32)
        instance.save(update_fields=["key1"])
