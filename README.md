# JustifAbs AIBD SA — version sécurisée

Application FastAPI de dépôt, traitement et suivi des justificatifs d'absence.

## Fonctions incluses

- Profils Agent, Manager, RH et Administrateur.
- Dépôt de pièces avec limite de taille, extensions autorisées, noms aléatoires et empreinte SHA-256.
- Workflow : soumis, complément requis, en cours, validé, rejeté.
- Messagerie liée au dossier et journal d'audit.
- Recherche et filtres par statut et site.
- Exports CSV, Excel et PDF.
- Gestion et désactivation des comptes.
- Changement obligatoire du mot de passe initial.
- Sessions signées et expirables, cookies sécurisés et protection CSRF.
- Notifications SMTP facultatives.
- Stockage persistant Render dans `/app/data`.

## Déploiement Render

1. Importer ce projet dans un dépôt GitHub **privé**.
2. Dans Render, ouvrir **New > Blueprint** et sélectionner le dépôt.
3. Avant la création du service, renseigner les variables secrètes demandées :
   - `BOOTSTRAP_ADMIN_EMAIL` : votre adresse administrateur ;
   - `BOOTSTRAP_ADMIN_PASSWORD` : au moins 10 caractères, majuscule, minuscule et chiffre.
4. Valider le Blueprint. Le service utilise le plan `starter` et un disque persistant de 1 Go.
5. Se connecter avec le compte administrateur, puis changer immédiatement le mot de passe.

La base est enregistrée dans `/app/data/aibd_absences.db` et les pièces dans `/app/data/uploads`.

## Installation locale

```bash
cp .env.example .env
# modifier au minimum SECRET_KEY et le compte administrateur
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
set -a; source .env; set +a
uvicorn main:app --reload
```

Ou avec Docker :

```bash
docker compose up --build
```

## Notifications Microsoft 365 facultatives

Définir `SMTP_HOST=smtp.office365.com`, `SMTP_PORT=587`, `SMTP_TLS=true`, ainsi que `SMTP_USER`, `SMTP_PASSWORD` et `SMTP_FROM`. Pour un environnement institutionnel, privilégier un compte de service et les règles de sécurité validées par AIBD SA.

## Avant exploitation réelle

Faire valider le traitement par les fonctions RH, juridique, sécurité SI et protection des données. Prévoir sauvegardes chiffrées, antivirus des fichiers, politique de conservation, supervision, SSO Microsoft Entra ID et, à terme, PostgreSQL avec stockage objet.
