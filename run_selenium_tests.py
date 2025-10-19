"""
Script pour lancer les tests Selenium de l'application JO Tickets.
Usage:
    python run_selenium_tests.py
"""
import os
import sys
import subprocess
import time
import requests


def start_django_server():
    """Démarre le serveur Django en arrière-plan."""
    print("🚀 Démarrage du serveur Django...")
    process = subprocess.Popen(
        ["python", "manage.py", "runserver", "127.0.0.1:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Attendre que le serveur soit prêt
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://127.0.0.1:8000/", timeout=2)
            if response.status_code == 200:
                print("Serveur Django démarré avec succès")
                return process
        except Exception:
            time.sleep(1)

    print("Impossible de démarrer le serveur Django")
    process.terminate()
    return None


def wait_for_server():
    """Attend que le serveur soit accessible."""
    print("Attente du serveur Django...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://127.0.0.1:8000/", timeout=2)
            if response.status_code == 200:
                print("Serveur Django accessible")
                return True
        except Exception:
            time.sleep(1)

    print("Serveur Django non accessible")
    return False


def run_selenium_tests():
    """Lance les tests Selenium."""
    print("Lancement des tests Selenium...")

    # Configuration Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jo_tickets.settings")

    # Lancer les tests Selenium
    command = [
        "python",
        "manage.py",
        "test",
        "tests.functional.test_user_registration.UserRegistrationSeleniumTest",
        "-v",
        "2",
    ]

    result = subprocess.run(command, capture_output=False)
    return result.returncode


def main():
    """Fonction principale."""
    print("Lancement des tests Selenium pour JO Tickets")
    print("=" * 50)

    # Vérifier si le serveur est déjà en cours d'exécution
    if wait_for_server():
        print("ℹServeur Django déjà en cours d'exécution")
        server_process = None
    else:
        # Démarrer le serveur Django
        server_process = start_django_server()
        if not server_process:
            print("Impossible de démarrer le serveur Django")
            return 1

    try:
        # Lancer les tests Selenium
        exit_code = run_selenium_tests()

        if exit_code == 0:
            print("Tous les tests Selenium sont passés avec succès!")
        else:
            print("Certains tests Selenium ont échoué.")

        return exit_code

    finally:
        # Arrêter le serveur Django si on l'a démarré
        if server_process:
            print("Arrêt du serveur Django...")
            server_process.terminate()
            server_process.wait()


if __name__ == "__main__":
    sys.exit(main())
