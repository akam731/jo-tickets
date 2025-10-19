## JO Tickets – Projet Bloc 3 Python

Application Django de billetterie pour les Jeux Olympiques.

Fonctionnalités principales:
- Authentification sécurisée (utilisateur, employé, administrateur)
- Catalogue d’offres, panier, paiement simulé, confirmation de commande
- Billets avec QR code et page détail; scan et validation côté employé
- Panneau d’administration

## Lien de l'application déployée

https://jo-tickets.onrender.com

---

## Démarrage rapide (local)

#### 1) Prérequis 
```
Python 3.12+, pip, venv.
```

#### 2) Clonage du repository
```bash
git clone https://github.com/akam731/jo-tickets.git
cd jo-tickets
```

#### 3) Créer le fichier d’environnement
Créez un fichier `.env.local` à la racine du projet avec des valeurs de développement. Voici un exemple :
```env
# Clé secrète Django
SECRET_KEY=modifier-la-cle-secrete

# Configuration de développement
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration base de données PostgreSQL
DB_NAME=nom_bdd
DB_USER=utilisateur_bdd
DB_PASSWORD=mot-de-passe_bdd
DB_HOST=hote_bdd
DB_PORT=port_bdd
```
#### 4) Installer les dépendances
```bash
python -m venv .venv
.venv/Scripts/activate # Windows (PowerShell)
# source .venv/bin/activate # Linux/macOS
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```
Une fois les dépendances installées il faut revenir à la racine du projet pour les prochaines commandes.

#### 5) Appliquer les migrations
```
python manage.py migrate
```

#### 6) Lancer le serveur
```
py manage.py runserver
```

Ouvrir: http://127.0.0.1:8000

Données de démo (offres):
```bash
python manage.py seed_offers
```

---

## Configuration

Variables d’environnement utiles (`.env.local`/`.env`):
- `SECRET_KEY` : Clé secrète de l'application (obligatoire)
- `DEBUG` (True en dev, False en prod)
- Base de données PostgreSQL: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

Static & Media:
- Static: WhiteNoise + Manifest (prod)
- QR codes: générés à la volée

---

## Déploiement Render (résumé)

1) Static: `python manage.py collectstatic --noinput` exécuté au build (Dockerfile).
2) QR codes: servis via la route `/billet/<id>/qr.png` (pas de stockage `media`).
3) Erreurs 4xx/5xx: `/erreur/<code>` pour visualiser les écrans.

---

## Tests

👉 [Voir la documentation des tests](tests/README.md)


---

## Structure

Routes clés:
- Accueil: `/`
- Offres: `/offres/`
- Panier: `/panier/`
- Finaliser: `/panier/finaliser/`
- Mes billets: `/mes-billets/`
- Détail billet: `/billet/<id>/`
- QR on-the-fly: `/billet/<id>/qr.png`
- Scan: `/scanner/` (employé)
- Tableau de bord : `/administration/` (admin)
- Erreurs: `/erreur/<code>`

---

## MCD

👉 [Voir le MCD (PNG)](docs/MCD.png)

---

## Documentation

👉 [Documentation technique](docs/documentation.md)

👉 [Manuel d'utilisation](docs/manuel.md)
