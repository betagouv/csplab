# CSPLab

⚠️ Ce projet est en cours de développement. ⚠️

## Objectif du projet

Accompagner le travail des employeurs de la fonction publique.

Plus d'information sur la page dédiée à notre startup d'état 👉
https://beta.gouv.fr/startups/csplab.html

## 🏗️ Architecture

Le monorepo est organisé en services :

- **dev** : Service pour les outils de développement
- **notebook** : Service Jupyter pour l'analyse et le prototypage

### Prérequis

- [mise](https://mise.jdx.dev/getting-started.html) : lanceur de tâches du repo ([docs/mise.md](docs/mise.md)), il installe et épingle lui-même les outils (node, pnpm, uv).
- Docker + Docker Compose (Colima, Docker Desktop, OrbStack…)
- [scw](https://www.scaleway.com/en/docs/scaleway-cli/quickstart/), installé par mise : les secrets des services sont lus dans Scaleway Secret Manager. `scw init` enregistre une [clé d'API](https://www.scaleway.com/en/docs/iam/how-to/create-api-keys/) et le projet CSPLab (identifiants fournis par l'équipe) dans `~/.config/scw/config.yaml`.
- [poppler](https://poppler.freedesktop.org/) : requis pour le service OCR en local (géré automatiquement en production via l'`Aptfile`)
- [tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html) avec le pack de langue française (`tesseract-lang` sur macOS, `tesseract-ocr-fra` sur Linux) — requis pour le service OCR en local (géré automatiquement en production via l'`Aptfile`)

### Optionnel

- [commitizen](https://commitizen-tools.github.io/commitizen/)

## Installation de l'environnement de dev

```bash
git clone <repository-url>
cd csplab
mise run onboard
```

La commande `onboard` créés les fichiers d'environnement depuis les exemples, installe les git hooks, les services docker, les dépendances, les migrations et créé un superuser.
Les étapes qui la composent sont disponibles séparément (`mise run setup`, `mise run git-hooks`, `mise run bootstrap`) et sont idempotentes.
Pour repartir de zéro sur une machine existante (fichiers d'env réinitialisés, bases locales recréées) : `mise run onboard:reset`.

### Configuration

Les fichiers `env.d/*`, créés depuis les exemples, portent la configuration locale (ports, bases Docker, `SCALEWAY_ENV=dev`). Les secrets viennent de Scaleway Secret Manager et sont injectés par mise à chaque tâche : `mise run secrets:check` vérifie l'accès et liste ce qui est disponible. Détail dans [docs/mise.md](docs/mise.md), section Secrets.

Pour personnaliser Docker Compose (ex : changer les ports), voir [docs/docker_compose_override.md](docs/docker_compose_override.md).

🤓 développement ...

```bash
mise run lint:fix
git add .
bin/cz commit
```

`bin/cz` encadre la rédaction de message de commit au format du projet ; `mise run lint` vérifie le tout avant de pousser.

### Format des messages de commit

Les messages de commit doivent respecter le format gitmoji configuré :

```
<emoji>(<scope>) <subject>
<body>
<footer>
```

**Exemples :**

- `✨(auth) add support for HTTP basic auth`
- `🐛(api) fix user authentication bug`
- `📝(docs) update installation guide`
