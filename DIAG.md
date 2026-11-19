# Diagnostic de l'ATS en dev

Cette branche sert à trouver pourquoi l'ATS reste vide avec `mise run dev` alors que `mise run web:emulate-prod` l'affiche. On la supprime après le diagnostic.

Chaque essai passe par un profil mise, activé par la variable `MISE_ENV` ([documentation](https://mise.jdx.dev/configuration/environments.html)). Ton `mise.local.toml` reste chargé. Les profils sont `diag` (tâches de diagnostic), `ipv4` et `ports`.

## Préparer le checkout

```bash
git fetch origin diag/ats-dev-linux
git switch diag/ats-dev-linux
MISE_ENV=diag mise run diag:prepare
```

`diag:prepare` crée à partir des exemples les fichiers `env.d/*` qui manquent, installe les dépendances de `src/web` et applique les migrations. Pour chaque essai, tu lances la pile dans un premier terminal, tu ouvres l'adresse indiquée dans le navigateur, puis tu lances le diagnostic dans un second terminal.

## Essai 1 : configuration actuelle

Tu passes sur le commit qui précède le correctif candidat, puis tu lances la pile habituelle.

```bash
git switch --detach diag/ats-dev-linux~1
mise run dev
```

Ouvre http://127.0.0.1:8000/ats/, puis http://localhost:8000/ats/, puis la même adresse dans une fenêtre privée, où les extensions sont désactivées. Pour chaque page, note si l'ATS s'affiche et copie les erreurs de la console (F12, onglet Console), puis lance :

```bash
MISE_ENV=diag mise run diag
```

## Essai 2 : Django et Vite sur 127.0.0.1

Toujours sur `diag/ats-dev-linux~1`.

```bash
MISE_ENV=ipv4 mise run dev
MISE_ENV=diag,ipv4 mise run diag
```

Adresse : http://127.0.0.1:8000/ats/

## Essai 3 : autres ports

Toujours sur `diag/ats-dev-linux~1`. Django écoute sur 8123 et Vite sur 5273.

```bash
MISE_ENV=ports mise run dev
MISE_ENV=diag,ports mise run diag
```

Adresse : http://localhost:8123/ats/

## Essai 4 : correctif candidat

Le dernier commit de la branche donne par défaut à Vite l'origine `http://127.0.0.1:5173` et le fait écouter sur l'hôte de cette origine.

```bash
git switch diag/ats-dev-linux
mise run dev
MISE_ENV=diag mise run diag
```

Adresse : http://127.0.0.1:8000/ats/, puis http://localhost:8000/ats/

## Causes possibles et indices dans la sortie

- Vite écoute sur `::1` et le navigateur demande `127.0.0.1`, ou l'inverse : la section des sockets montre Vite sur une seule famille d'adresses, et la section des scripts montre un échec en `-4` ou en `-6`. Les essais 2 et 4 corrigent ce cas.
- Un autre serveur répond sur le port de Vite ou de Django, par exemple le Vite d'un autre projet sur 5173 : la section des sockets nomme son dossier, et `main.ts` est signalé « NOT the csplab entry ». On arrête ce serveur, ou on passe par l'essai 3.
- Une variable `PORT` ou `HOST` exportée par le shell déplace Vite, qui lit les mêmes variables que Django : la section des variables les affiche. On les retire du shell avant de lancer la pile.
- Un proxy HTTP intercepte `localhost` : la sortie signale les variables de proxy et affiche `no_proxy`, qui doit contenir `localhost` et `127.0.0.1`.
- Vite s'arrête au démarrage, par exemple faute de watchers inotify : aucune socket sur son port, l'erreur est dans le terminal de la pile, et la section inotify donne les limites.
- La page est ouverte sur une autre adresse que `localhost` ou `127.0.0.1` (nom de la machine, IP du réseau, `0.0.0.0`) : le CORS de Vite refuse les scripts. On ouvre les adresses indiquées.
- Une extension du navigateur bloque les scripts d'un autre port : l'ATS s'affiche en fenêtre privée.

## Ce qu'on attend en retour

Pour chaque essai : l'ATS s'affiche ou non, les erreurs de la console et la sortie complète de `mise run diag`. La sortie n'affiche aucun secret, seulement la présence des variables de proxy.

Après les essais, `git status` doit être propre. Si mise a réécrit `mise.lock`, on annule par `git checkout -- mise.lock`, puis on revient sur sa branche habituelle.
