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

- Docker
- Docker Compose
- GNU Make

### Optionnel

[commitizen](https://commitizen-tools.github.io/commitizen/)

## Installation de l'environnement de dev

```bash
git clone <repository-url>
cd csplab
make bootstrap
make run-notebook
```

Pour installer les git hooks (pre-commit et commit-msg):

```bash
make git-hooks
```

🤓 développement ...

```bash
make lint-fix
git add .
bin/cz commit
```

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
