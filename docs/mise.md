# Tâches mise

Ce projet utilise [mise](https://mise.jdx.dev/tasks/) pour lancer les tâches localement et dans la CI exécute aussi.

`mise install` installe les outils (node, uv, scw).

`mise run` seul affiche les commandes usuelles

`mise tasks --all` liste toutes les tâches.

## Organisation

Chaque sous-projet (`src/web`, son frontend, `src/ocr`, `src/ingestion`, `src/notebook`, `libs/ddd`, `libs/referentiel`) déclare ses tâches et son environnement dans son propre `mise.toml`. Les mêmes noms de tâches existent dans chaque sous-projet :

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

Chaque tâche de sous-projet a aussi un alias plus court, sans quotes : le nom du projet suivi du nom de la tâche. `web:dev`, `web:manage`, `front:build`, `ocr:test`, `ingestion:migrate`, `ddd:lint`, etc. Le frontend (`src/web/presentation/frontend`) a le préfixe `front`. Un alias se résout depuis la racine ou depuis le dossier du projet qui le définit ; depuis un autre sous-projet, utilisez le chemin complet (`mise run '//src/ocr:test'`), qui fonctionne partout.

```
mise run web:dev
mise run web:manage -- shell
mise run web:test -- -k organisme
mise run ingestion:test
```

Le `mise.toml` à la racine contient ce qui concerne le repo entier :

- `lint`, `lint:fix`, `test`, `test:cov`, `check`, `install` : lancent la tâche correspondante de tous les sous-projets, plus celles du frontend. Un nouveau sous-projet ajouté à `config_roots` y est inclus automatiquement.
- `services:postgres`, `services:redis`, `services:qdrant`, `services` : démarrent les conteneurs docker. Les tâches qui ont besoin d'un service le déclarent en dépendance, il démarre donc tout seul.
- `onboard` : premier embarquement (setup + git-hooks + bootstrap). `setup`, `git-hooks` et `bootstrap` restent disponibles séparément, et `bootstrap:reset` repart de zéro (volumes docker supprimés puis bootstrap).

Les opérations sur la base de dev sont dans le namespace web : `web:seed` charge le jeu de données de démo, `web:db:reset` recrée la base à vide puis migre et seed, `web:db:restore` la remplace par un dump Scalingo.

Pour observer ou arrêter les conteneurs, utilisez `docker compose` directement (`ps`, `logs -f`, `stop`, `down`).

## Outils

Le `mise.toml` racine déclare les outils dans `[tools]` et `mise.lock` épingle pour chacun la version exacte, l'URL et la somme de contrôle, pour toutes les plateformes. `mise outdated` liste les mises à jour disponibles ; `mise up` les applique dans la plage déclarée (`mise up --bump` élargit la plage) et réécrit `mise.lock`, à committer avec le changement. `mise doctor` et `mise cfg` montrent l'état de l'installation et les fichiers de configuration chargés. `pnpm` vient des shims corepack de node ; un node installé avant le réglage `node.corepack` ne les a pas, `mise x -- corepack enable` les crée.

## Environnement

Le `mise.toml` de chaque sous-projet charge son fichier `env.d/*` et active son `.venv` (section `[env]`). Une tâche s'exécute donc avec le bon environnement quel que soit le dossier courant. Dans un shell interactif, `mise activate` charge cet environnement à chaque changement de dossier, et `mise en src/web` ouvre un sous-shell avec l'environnement complet du service, secrets compris.

En dev, les pages ATS chargent leurs assets depuis le serveur Vite, pas depuis le build : `mise run dev` lance les deux (Django + Vite HMR) ; `web:dev` et `front:dev` restent disponibles séparément. Le build n'est utilisé que quand `debug` est désactivé, notamment par les tests e2e, qui le régénèrent en dépendance.

## Secrets

Chaque service lit ses secrets dans Scaleway Secret Manager, sous `/{service}/{SCALEWAY_ENV}` (`/web/dev`, `/ingestion/dev`, `/ocr/dev`). La directive `_.source` de la section `[env]` les charge quand mise calcule l'environnement du service : toutes ses tâches et le shell activé en disposent. Le calcul a lieu à l'entrée dans le dossier et à chaque changement de configuration.

Prérequis, une fois par machine : `scw init` avec le projet et la région CSPLab (`mise install` fournit la commande `scw`). Les identifiants sont stockés dans `~/.config/scw/config.yaml`. Les variables `SCW_*`, si elles sont définies, ont priorité : c'est le mode utilisé sur Scalingo. Sans `SCALEWAY_ENV`, le chargement est ignoré et la CI fournit ses valeurs dans `mise.ci.toml`.

`mise run secrets:check` vérifie l'accès et liste les noms des secrets de chaque service.

Les tâches de test chargent `env.test` (valeurs factices, versionnées) et tournent sans accès à Scaleway. `mise.ci.toml` charge le même fichier.

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

## CI

Tous les workflows sélectionnent l'environnement `MISE_ENV=ci` via l'action `setup-mise`, qui charge `mise.ci.toml` par-dessus `mise.toml`, qui remplace les tâches `services:*` par des no-ops, les services étant fournis par les containers du workflow. `src/ingestion/mise.ci.toml` neutralise en plus ses tâches `db:create*` et pointe `DATABASE_URL`/`TEST_DATABASE_URL` vers le service Postgres du job. `src/ocr/mise.ci.toml` fournit l'`API_KEY` et `src/web/mise.ci.toml` l'environnement Django, que `env.d/*` (non versionnés) portent en local.

`MISE_ENV=ci mise run web:test`, `MISE_ENV=ci mise run ingestion:test` ou `MISE_ENV=ci mise run ocr:test` reproduisent ce contexte en local.
