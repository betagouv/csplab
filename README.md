# CSPLab

⚠️ Ce projet est en cours de développement. ⚠️

## Objectif du projet

Accompagner le travail des employeurs de la fonction publique.

Plus d'information sur la page dédiée à notre startup d'état 👉
https://beta.gouv.fr/startups/csplab.html

## 🏗️ Architecture

Le monorepo est organisé en services :

- **notebook** : Service Jupyter pour l'analyse et le prototypage

### Prérequis

- [mise](https://mise.jdx.dev/getting-started.html) : lanceur de tâches du repo ([docs/mise.md](docs/mise.md)), il installe et épingle lui-même les outils déclarés dans la section `[tools]` de `mise.toml`.
- Docker + Docker Compose (Colima, Docker Desktop, OrbStack…)
- [scw](https://www.scaleway.com/en/docs/scaleway-cli/quickstart/), installé par mise : les secrets des services sont lus dans Scaleway Secret Manager. `scw init` enregistre une [clé d'API](https://www.scaleway.com/en/docs/iam/how-to/create-api-keys/) et le projet CSPLab (identifiants fournis par l'équipe) dans `~/.config/scw/config.yaml`.
- [poppler](https://poppler.freedesktop.org/) : requis pour le service OCR en local (géré automatiquement en production via l'`Aptfile`)
- [tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html) avec le pack de langue française (`tesseract-lang` sur macOS, `tesseract-ocr-fra` sur Linux) — requis pour le service OCR en local (géré automatiquement en production via l'`Aptfile`)

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
git commit
```

Le hook commit-msg vérifie le format de chaque message de commit, et la CI celui du titre de PR. `mise x -- cz commit`, facultatif, remplace `git commit` en posant les questions qui composent le message. `mise run lint` vérifie le tout avant de pousser.

### Format des messages de commit

Les commits et les titres de PR suivent le format [Conventional Commits](https://www.conventionalcommits.org/), en français :

```
<type>(<scope>): <subject>
```

Types autorisés : `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Le changelog range les entrées par scope ; la liste des scopes est donc fermée, et un scope hors liste est refusé au commit comme au titre de PR :

| Scope | Périmètre |
|---|---|
| `recruteur` | Espace recruteur |
| `candidatures` | Candidatures et parcours candidat |
| `messages` | Messagerie |
| `identite` | Authentification et comptes |
| `ingestion` | Service d'ingestion |
| `referentiel` | Données de référence |
| `ocr` | Service OCR |
| `notebook` | Notebooks d'analyse |
| `tooling` | Outillage de développement, CI |
| `release` | Versions et changelog |

Un changement technique (`web`, `front`, `ui`…) prend le scope du domaine fonctionnel qu'il touche. La liste est déclarée deux fois dans `cz.toml` (le motif `schema_pattern` et les choix de la question `scope`) : modifier les deux ensemble.

**Exemples :**

- `feat(identite): ajoute le support de l'authentification HTTP basic`
- `fix(recruteur): corrige le filtre des offres`
- `docs(tooling): met à jour le guide d'installation`
