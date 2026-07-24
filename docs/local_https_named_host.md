# Servir l'ATS sur un hôte HTTPS local nommé

Par défaut, l'ATS tourne sur `http://localhost:8000` et charge Vite depuis
`http://localhost:5173`. On peut aussi le servir derrière un nom stable en HTTPS
(ex. `https://csplab.localhost`, sans port). Le dépôt ne code aucun hôte en dur ;
le reverse-proxy (Caddy, Traefik, valet + portless…) reste propre à chaque machine.

## Contrat pour servir l'ATS sur un hôte HTTPS local nommé, quel que soit le reverse-proxy

1. **Origine Vite** : pointer `WEB_VITE_DEV_ORIGIN` (lue par Vite et Django) vers
   l'hôte public. Une origine `https://` bascule Vite en reverse-proxy (HMR `wss`)
   et adapte la CSP dev :

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

## Exemple : portless

En utilisant [portless](https://www.npmjs.com/package/portless), on peut :

1. Configurer un alias via `portless alias csplab 8000`

2. Référencer des tâches dans un fichier `mise.local.toml` (gitignoré) qui surchargeront le `mise.local` versionné :
- `front:portless` : Vite via portless, `WEB_VITE_DEV_ORIGIN=https://vite.csplab.localhost` ;
- `back:portless` : `make run-web` avec la même origine ;
- `open:portless` : attend le back puis ouvre `https://csplab.localhost` ;
- `dev` : override du `dev` versionné vers les trois ci-dessus.

Résultat : `mise dev` prépare, sert et ouvre l'ATS sur `https://csplab.localhost`.
