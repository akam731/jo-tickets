# Guide Utilisateur - JO Tickets

## Comptes demo

### Comptes utilisateur
| Adresse e-mail        | Mot de passe |
|-----------------------|--------------|
| client@jotickets.com  | User123!     |
| client2@jotickets.com | User123!     |
| client3@jotickets.com | User123!     |


### Comptes employés
> **Note** : Pour des raisons de sécurité, le compte employé de démonstration est fourni directement dans ma copie.

### Comptes administrateur
> **Note** : Pour des raisons de sécurité, le compte administrateur de démonstration est fourni directement dans ma copie.


## Pré-requis

### Compte utilisateur
- Adresse email valide
- Mot de passe sécurisé (minimum 8 caractères)
- Nom et prénom

### Accès à l'application
- **URL locale** : http://127.0.0.1:8000/
- **URL démo** : https://jo-tickets.onrender.com/
- **Navigateurs recommandés** : Chrome, Firefox

---

## Création d'un compte

### 1. Accéder au formulaire d'inscription
1. Cliquez sur [**S'inscrire**](https://jo-tickets.onrender.com/inscription/) depuis la barre de navigation
2. Remplissez le formulaire d'inscription

### 2. Règles de mot de passe
- **Minimum 8 caractères**
- **Recommandé** : Majuscules, minuscules, chiffres et symboles
- **Exemple valide** : `MonMotDePasse123!`

### 3. Validation du compte
- Connectez-vous avec vos identifiants depuis la page de [**Connexion**](https://jo-tickets.onrender.com/connexion/) visible dans la barre de navigation

---

## Parcourir les offres

Cliquez sur [**Offres**](https://jo-tickets.onrender.com/offres/) depuis la barre de navigation

### Types d'offres disponibles par défaut

#### Solo (1 personne)
- **Prix** : 25€
- **Capacité** : 1 personne
- **Idéal pour** : Visite individuelle

#### Duo (2 personnes)
- **Prix** : 45€
- **Capacité** : 2 personnes
- **Idéal pour** : Couples, amis

#### Familiale (4 personnes)
- **Prix** : 80€
- **Capacité** : 4 personnes
- **Idéal pour** : Familles

### Ajouter au panier
1. **Sélectionnez** l'offre
2. **Cliquez** sur "Ajouter au panier"
> **Note** : Il faut être connecté pour avoir accès à son panier.


---

## Validation de la commande

Cliquez sur [**Panier**](https://jo-tickets.onrender.com/panier/) depuis la barre de navigation pour accéder à votre panier.

### 1. Vérification du panier
- **Articles** : Vérifiez les offres sélectionnées
- **Quantités** : Contrôlez les nombres
- **Total** : Vérifiez le montant final

### 2. Procédure de paiement
1. **Cliquez** sur "Finaliser la commande"
2. **Sélectionnez** une méthode de paiement (Carte bancaire / PayPal)
3. **Cliquez** sur "Payer XX €"

> **Note** : Le paiement est simulé pour la démonstration. Aucun vrai paiement n'est effectué.

### 3. Confirmation
- **Message de succès** : "Paiement effectué avec succès"
- **Redirection** : Vers la page [**Mes Billets**](https://jo-tickets.onrender.com/mes-billets/)

---

## Récupération du e-billet

### 1. Accès aux billets
1. [**Connectez-vous**](https://jo-tickets.onrender.com/connexion/) à votre compte
2. **Cliquez** sur [**Mes Billets**](https://jo-tickets.onrender.com/mes-billets/) dans le menu
3. **Sélectionnez** le billet à visualiser "Voir détails"

### 2. Informations du billet
- **QR Code** : Code à scanner à l'entrée (généré automatiquement à l'affichage)
- **Clé finale** : Identifiant unique du billet
- **Statut** : Valide/Utilisé
- **Détails** : Offre, date d'achat ...

### 3. Actions disponibles
- **Copier la clé** : Clé disponible sous le QR Code
- **Présenter** le QR code ou la clé au contrôle

---

## Espace Administrateur

> **Note** : L'espace administration n\'est disponible que pour les utilisateur bénéficiant du statut d'administrateur
 
### Accès
- **Lien** : [**Administration**](https://jo-tickets.onrender.com/administration/) disponible dans la barre de navigation

### Statistiques de ventes
- **Ventes par offre** : Revenus propres à chaque offre
- **Revenus totaux** : Montant des ventes
- **Billets vendus** : Nombre total
- **Offres actives** : Nombre d'offres actives

Cliquez sur [**Gérer les offres**](https://jo-tickets.onrender.com/administration/offres/) depuis l'espace administration

### Gestion des offres (CRUD)
#### Créer une offre
1. **Cliquez** sur "Nouvelle offre"
2. **Remplissez** : Nom, capacité, prix, description
3. **Activez** l'offre si nécessaire
4. **Sauvegardez**

#### Modifier une offre
1. **Sélectionnez** l'offre à modifier
2. **Cliquez** sur "Modifier"
3. **Ajustez** les informations
4. **Sauvegardez**

#### Supprimer une offre
1. **Sélectionnez** l'offre
2. **Cliquez** sur "Supprimer"
3. **Confirmez** la suppression

---

## Espace Employé (Scan)

### Accès
- **Lien** : [**Scanner**](https://jo-tickets.onrender.com/controle/scanner/) disponible dans le menu

### Scanner un QR code
1. **Autorisez** l'accès à la caméra
2. **Positionnez** le QR code dans le cadre
3. À la première lecture, le scan s'arrête automatiquement (évite les doublons)
4. **Relancer le scan**: bouton "Relancer le scan"

### Saisie manuelle
1. **Copiez** la clé finale du billet
2. **Collez** dans le champ de saisie
3. **Cliquez** sur "Valider le billet"

### Résultats du scan

#### Billet valide
- **Statut** : Validé avec succès
- **Propriétaire** : Nom du détenteur
- **Offre** : Type d'offre
- **Date d'achat** : Date d'achat du billet

#### Billet déjà utilisé
- **Statut** : Déjà utilisé
- **Informations** : Détails du billet

#### Billet invalide
- **Statut** : Billet introuvable
- **Vérification** : Vérifiez la clé saisie