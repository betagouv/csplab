# Servir l'ATS sur un hôte HTTPS local nommé

Par défaut, l'ATS tourne sur `http://localhost:8000` et charge Vite depuis `http://localhost:5173`. On peut aussi le servir derrière un nom stable en HTTPS (ex. `https://csplab.localhost`, sans port). Le dépôt ne code aucun hôte en dur dans sa configuration par défaut ; chacun choisit son reverse-proxy (Caddy, Traefik, valet, portless…). Pour portless, le dépôt fournit une configuration optionnelle, décrite plus bas.

## Contrat pour servir l'ATS sur un hôte HTTPS local nommé, quel que soit le reverse-proxy

1. **Origines** : `WEB_VITE_DEV_ORIGIN` (lue par Vite et Django) pointe vers
   l'hôte Vite public. Une origine `https://` bascule Vite en reverse-proxy
   (HMR `wss`) et adapte la CSP dev. Le CORS de Vite accepte d'office les hôtes
   locaux (`localhost`, `*.localhost`, `127.0.0.1`) ; pour servir la page depuis
   un hôte hors de cette liste (ex. `csplab.test`), ajouter `WEB_ATS_ORIGIN`
   avec l'origine de la page :

   ```
   WEB_VITE_DEV_ORIGIN=https://vite.csplab.localhost
   ```

2. **Router les hôtes** via le proxy :
- `csplab.localhost` : Django `:8000`,
- `vite.csplab.localhost` : serveur Vite.

3. **Autoriser hôte + CSRF** dans `env.d/web` :

   ```
   WEB_ALLOWED_HOSTS=.localhost,127.0.0.1,0.0.0.0
   WEB_CSRF_TRUSTED_ORIGINS=https://csplab.localhost
   ```

## Configuration portless

[portless](https://github.com/vercel-labs/portless) donne un nom `.localhost` en HTTPS à chaque serveur de dev, sur un port choisi par lui. `MISE_ENV=portless mise install` l'installe avec les autres outils du dépôt. Au premier lancement d'une tâche, portless démarre son proxy, crée une autorité de certification locale et peut demander le mot de passe de la session. En option, `portless service install` démarre le proxy avec la machine ; on relance cette commande après une mise à jour de Node, car le service appelle Node par son chemin complet.

L'environnement mise `portless` charge `mise.portless.toml` et `src/web/mise.portless.toml` par-dessus la configuration par défaut :

- `mise run dev` sert Django sur `https://csplab.localhost` et Vite sur `https://vite.csplab.localhost` ;
- `mise run sb` sert Storybook sur `https://storybook.csplab.localhost` ;
- `WEB_VITE_DEV_ORIGIN` et `WEB_CSRF_TRUSTED_ORIGINS` suivent ces noms, par-dessus `env.d/web`.

Dans un worktree git, portless préfixe chaque nom par le dernier segment de la branche (`https://<branche>.csplab.localhost`), ce qui permet de servir plusieurs branches en même temps. Un worktree sans branche garde les noms du clone principal.

On active l'environnement par commande (`MISE_ENV=portless mise run dev`) ou pour toutes ses commandes, en exportant `MISE_ENV=portless` dans son shell. Un `mise.local.toml` qui définit des tâches de même nom (`dev`, `sb`…) se mêle à celles de `mise.portless.toml` : on les retire de son `mise.local.toml`.
