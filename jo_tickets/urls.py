from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse
from django.conf.urls import handler400, handler403, handler404, handler500


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("", include("apps.catalog.urls")),
    path("", include("apps.cart.urls")),
    path("", include("apps.orders.urls")),
    path("", include("apps.tickets.urls")),
]


def error_view(request, exception=None, status_code=500, message=None):
    context = {
        "status_code": status_code,
        "message": message,
    }
    return render(request, "errors/error.html", context, status=status_code)


# Handlers d'erreurs personnalisés
handler400 = lambda request, exception=None: error_view(request, exception, 400, "Requête invalide.")
handler403 = lambda request, exception=None: error_view(request, exception, 403, "Accès refusé.")
handler404 = lambda request, exception=None: error_view(request, exception, 404, "Page non trouvée.")
handler500 = lambda request: error_view(request, None, 500, "Erreur interne du serveur.")


