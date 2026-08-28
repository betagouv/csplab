# Tâches mise

Le Makefile a été remplacé par des tâches [mise](https://mise.jdx.dev/tasks/),
que la CI exécute aussi : le workflow `web.yml` sélectionne l'environnement
`MISE_ENV=ci`, qui charge `mise.ci.toml` par-dessus `mise.toml` (même mécanique
que `mise.local.toml`). Ce fichier porte l'env de la CI et remplace les tâches
`services:*` par des no-ops, les services étant fournis par les containers du
workflow. `MISE_ENV=ci mise run web:test` reproduit ce contexte en local.
`mise install` installe les outils (node, uv). `mise run` seul affiche les
commandes usuelles, `mise tasks --all` liste toutes les tâches.

## Organisation

Chaque sous-projet (`src/web`, son frontend, `src/ocr`, `src/ingestion`,
`src/notebook`, `libs/ddd`, `libs/referentiel`) déclare ses tâches et son environnement dans
son propre `mise.toml`. Les mêmes noms de tâches existent dans chaque
sous-projet :

- `install` : installer ses dépendances
- `dev` : lancer son serveur de dev (web = runserver, ocr = uvicorn, etc.)
- `test`, et selon le projet `test:e2e`, `test:a11y`, `test:cov`
- `lint` : toutes ses vérifications statiques, en parallèle
- `lint:fix` : les corrections automatiques

S'y ajoutent des tâches propres à chaque projet, par exemple `migrate`,
`superuser` et `emulate-prod` pour le web, `jupytext:md` pour le notebook.

Trois façons de lancer une tâche :

```
mise run :test                 # depuis le dossier du sous-projet
mise run '//src/web:test'      # depuis n'importe où
mise run '//...:test'          # la même tâche dans tous les sous-projets
```

Chaque tâche de sous-projet a aussi un alias plus court, sans quotes : le nom
du projet suivi du nom de la tâche. `web:dev`, `web:manage`, `front:build`,
`ocr:test`, `ingestion:migrate`, `ddd:lint`, etc. Le frontend
(`src/web/presentation/frontend`) a le préfixe `front`. Un alias se résout
depuis la racine ou depuis le dossier du projet qui le définit ; depuis un
autre sous-projet, utilisez le chemin complet (`mise run '//src/ocr:test'`),
qui fonctionne partout.

```
mise run web:dev
mise run web:manage -- shell
mise run web:test -- -k organisme
mise run ingestion:test
```

Le `mise.toml` à la racine contient ce qui concerne le repo entier :

- `lint`, `lint:fix`, `test`, `test:cov`, `check`, `install` : lancent la
  tâche correspondante de tous les sous-projets, plus celles du frontend.
  Un nouveau sous-projet ajouté à `config_roots` y est inclus automatiquement.
- `services:postgres`, `services:redis`, `services:qdrant`, `services` :
  démarrent les conteneurs docker. Les tâches qui ont besoin d'un service le
  déclarent en dépendance, il démarre donc tout seul.
- `onboard` : premier embarquement (setup + git-hooks + bootstrap). `setup`,
  `git-hooks` et `bootstrap` restent disponibles séparément, et
  `bootstrap:reset` repart de zéro (volumes docker supprimés puis bootstrap).

Les opérations sur la base de dev vivent dans le namespace web : `web:seed` charge le jeu de données de démo, `web:db:reset` recrée la base à vide puis migre et seed, `web:db:restore` la remplace par un dump Scalingo.

Pour observer ou arrêter les conteneurs, utilisez `docker compose` directement (`ps`, `logs -f`, `stop`, `down`).

## Environnement

Le `mise.toml` de chaque sous-projet charge son fichier `env.d/*` et active son `.venv` (section `[env]`). Une tâche s'exécute donc avec le bon environnement quel que soit le dossier courant, sans direnv. Les `.envrc` restent utilisables pour avoir cet environnement dans un shell interactif.

En dev, les pages ATS chargent leurs assets depuis le serveur Vite, pas depuis le build : `mise run dev` lance les deux (Django + Vite HMR) ; `web:dev` et `front:dev` restent disponibles séparément. Le build n'est utilisé que quand `debug` est désactivé, notamment par les tests e2e, qui le régénèrent en dépendance.

## Détection de changements

Certaines tâches comparent leurs fichiers d'entrée et de sortie et ne s'exécutent que si nécessaire : le build du frontend, le build Storybook, les `install` (relancés quand `uv.lock` ou `pnpm-lock.yaml` change) et la conversion jupytext. Les tâches `dev` et `test` dépendent de `install` : après un pull qui change un lockfile, les dépendances se mettent à jour toutes seules au prochain lancement.

Les tâches d'un agrégat s'exécutent en parallèle. Les accès partagés sont sûrs : chaque suite de tests a sa propre base, et les tâches qui utilisent un venv ou node_modules déclarent leur `install` en dépendance (exécuté une seule fois par lancement, quelques millisecondes quand rien n'a changé). Pour forcer une exécution séquentielle, par exemple sur une machine chargée : `mise run check --jobs 1`.

## Tâches destructrices

`setup:force`, `bootstrap:reset`, `onboard:reset` (les deux précédents enchaînés), `web:db:reset` et `web:db:restore` demandent une confirmation dont la réponse par défaut est No : un Entrée par réflexe ne détruit rien, il faut répondre y explicitement. Attention aux lanceurs qui positionnent MISE_YES (boutons d'éditeur) : ils sautent la confirmation.

## Arguments

Ce qui suit `--` est passé à la commande :

```
mise run web:test -- tests/infrastructure/ -k organisme
mise run web:test:e2e -- --headed
```

## Préférences personnelles

`mise.local.toml` (gitignoré) permet de définir ses propres tâches et
raccourcis sans les imposer au repo :

```toml
# remplacer la stack dev par la sienne (reverse-proxy, navigateur auto...)
[tasks.dev]
depends = ["back:portless", "front:portless"]

# raccourci perso
[tasks.mytask]
alias = "mt"
```
