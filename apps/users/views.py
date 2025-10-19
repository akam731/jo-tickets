from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, UserLoginForm


class SignUpView(CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:home")
    template_name = "users/signup.html"

    def form_valid(self, form):

        response = super().form_valid(form)

        # Connecter automatiquement l'utilisateur
        user = form.instance
        login(self.request, user)

        messages.success(
            self.request,
            f"Bienvenue {user.get_full_name()} ! Votre compte a été créé avec succès.",
        )
        return response


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.get_full_name()} !")
                return redirect("users:home")
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect("users:home")


@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})


def home_view(request):
    return render(request, "home.html")


def construction_view(request):
    return render(request, "construction.html")


def maintenance_view(request):
    return render(request, "construction.html")
