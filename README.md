# JustifAbs AIBD SA

Application FastAPI de dépôt et de suivi des justificatifs d'absence.

## Correction Render intégrée

L'arborescence attendue est désormais incluse dans l'image Docker :

```text
static/style.css
templates/base.html
templates/login.html
...
```

Les chemins sont calculés à partir de l'emplacement réel de `main.py`. L'application ne dépend donc plus du répertoire courant du conteneur. Le disque Render `/app/data` conserve la base SQLite et les fichiers téléversés.

## Déploiement Render

1. Remplacer le contenu du dépôt GitHub par le contenu de cette archive.
2. Vérifier que `static/` et `templates/` apparaissent bien dans GitHub.
3. Dans Render, ouvrir le Blueprint puis lancer **Manual Sync**.
4. Saisir les valeurs demandées :
   - `BOOTSTRAP_ADMIN_EMAIL`
   - `BOOTSTRAP_ADMIN_PASSWORD` — au moins 12 caractères
5. Attendre le message `Your service is live`.

Le premier administrateur est créé uniquement si la base ne contient encore aucun utilisateur. Le mot de passe n'est pas enregistré dans le dépôt.

## Déploiement local avec Docker

```bash
docker compose up --build
```

Puis ouvrir `http://localhost:8000`.

## Contrôles effectués

- compilation syntaxique de `main.py` ;
- présence obligatoire de `static/style.css` et `templates/login.html` pendant la construction Docker ;
- chemins absolus pour les fichiers statiques et les modèles ;
- stockage persistant dans `/app/data` ;
- plan Render `starter`, compatible avec un disque persistant ;
- commande Uvicorn compatible avec la variable `PORT` de Render ;
- suppression des comptes de démonstration codés en dur.

## Sécurité institutionnelle

Avant utilisation avec de vraies données RH : dépôt GitHub privé, contrôle des habilitations, sauvegardes chiffrées, antivirus des pièces jointes, politique de conservation, registre de traitement et validation par les fonctions RH, juridique et protection des données.
