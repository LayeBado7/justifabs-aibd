# JustifAbs AIBD SA — version Render à fichiers plats

Cette version est conçue pour un téléversement depuis un téléphone ou une tablette lorsque GitHub place tous les fichiers à la racine.

## Fichiers indispensables à la racine

- `Dockerfile`
- `main.py`
- `embedded_assets.py`
- `requirements.txt`
- `render.yaml`

Les modèles HTML et la feuille de style sont intégrés dans `embedded_assets.py`. Au démarrage, l'application recrée automatiquement :

- `/app/templates/`
- `/app/static/`

Les anciens fichiers HTML ou CSS présents à la racine peuvent rester : ils ne bloquent pas le déploiement.

## Déploiement

1. Remplacer au minimum les cinq fichiers indispensables ci-dessus dans GitHub.
2. Vérifier que Render suit la branche par défaut du dépôt (`principal`).
3. Dans Render, lancer **Manual Sync**, puis **Clear build cache & deploy**.
4. Renseigner `BOOTSTRAP_ADMIN_EMAIL` et `BOOTSTRAP_ADMIN_PASSWORD`.
5. Le mot de passe administrateur doit contenir au moins 12 caractères.

Le point de contrôle est `/health`.
