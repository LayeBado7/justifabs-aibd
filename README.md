# JustifAbs AIBD SA

Application web complète de dépôt, traitement et suivi des justificatifs d'absence.

## Fonctionnalités

- Connexion sécurisée par profil : agent, RH, administrateur.
- Soumission d'une absence avec période, motif et pièces jointes.
- Formats autorisés : PDF, JPG, PNG, DOC et DOCX, avec limite configurable.
- Suivi des statuts : soumis, complément requis, en cours, validé, rejeté.
- Demandes de complément adressées à l'agent et réponses dans le dossier.
- Ajout ultérieur de pièces justificatives.
- Historique horodaté de toutes les opérations.
- Vérification SHA-256 de chaque fichier déposé.
- Tableau de bord RH et export CSV.
- Gestion des utilisateurs par l'administrateur.
- Déploiement Docker, Docker Compose ou Render.

## Démarrage local

```bash
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Ouvrir `http://localhost:8000`.

## Comptes de démonstration

- Agent : `agent@aibd.sn`
- RH : `rh@aibd.sn`
- Administrateur : `admin@aibd.sn`
- Mot de passe commun : `Aibd@2026`

Changez immédiatement ces comptes et la variable `SECRET_KEY` en production.

## Démarrage avec Docker

```bash
docker compose up --build
```

## Mise en ligne

### Render

1. Déposer le projet dans un dépôt GitHub privé.
2. Dans Render, créer un nouveau Blueprint à partir du dépôt.
3. Le fichier `render.yaml` configure le service et le disque persistant.
4. Pour une exploitation institutionnelle, utiliser PostgreSQL et un stockage objet compatible S3 plutôt que SQLite.

### Variables importantes

- `SECRET_KEY` : clé longue et aléatoire.
- `DATABASE_URL` : SQLite ou PostgreSQL.
- `UPLOAD_DIR` : dossier de stockage des justificatifs.
- `MAX_UPLOAD_MB` : taille maximale par fichier.
- `ALLOWED_EXTENSIONS` : extensions autorisées.
- `COOKIE_SECURE=true` derrière HTTPS.

## Sécurité et conformité à prévoir avant production

- Authentification AIBD via Microsoft Entra ID / Microsoft 365.
- Chiffrement des fichiers au repos et sauvegardes chiffrées.
- Antivirus lors du téléversement.
- Politique de conservation et purge automatique des justificatifs.
- Journalisation centralisée, supervision et alertes.
- Cloisonnement strict des rôles et revue périodique des habilitations.
- Registre de traitement, information des agents et validation par les fonctions RH, juridique et protection des données.

## Base juridique intégrée au cadrage

Le Code du travail sénégalais prévoit notamment la suspension du contrat pendant certaines absences, dont la maladie dûment constatée et les absences autorisées par l'employeur. L'application ne décide pas automatiquement de la validité juridique d'une absence : elle organise la collecte, le contrôle et la traçabilité des justificatifs.
