# ADR-010 : Sortir le frontend Vue de la couche `presentation`

**Status:** Proposé
**Date:** 2026.09.03
**Deciders:** Lucas P
**Tags:** frontend, monorepo, tooling

---

## Context

Le SPA Vue vit dans `src/web/presentation/frontend`. La couche `presentation/` de `src/web` est du code Python qui adapte le domaine vers HTTP ; le SPA est une application distincte qui consomme ce contrat. Le chemin encode une hiérarchie fausse et se répète dans l'outillage, la CI et l'espace de travail.

`src/web` porte une seconde surface navigateur, l'espace candidat (templates, JS vanilla, Sass compilé par `bin/sass`). Le tooling JavaScript des deux est déjà partagé par le package `csplab-web` à la racine de `src/web`, qui lint le JS candidat et les SCSS et délègue son `build` au SPA via un workspace pnpm.

### Contrats entre le SPA et `web`

- API : schéma OpenAPI `internal-schema.yaml` → `src/types/api.d.ts`, vérifié par `web:lint:types` ; format des erreurs de `custom_exception_handler` et des erreurs DRF par champ, lu par `api/errors.ts`.
- Hébergement : catch-all `/ats/` ; `templates/ats/base.html` monte l'entrée via `vite_tags`, qui lit `manifest.json` dans `static/frontend` ; en `DEBUG`, bascule vers `VITE_DEV_ORIGIN`.
- Authentification : session Django, cookie `csrftoken` posé par `@ensure_csrf_cookie`, en-tête `X-CSRFToken`, redirection vers `/utilisateur/connexion`, déconnexion par formulaire POST, `/utilisateur/me`.
- URLs Django écrites dans le SPA (`/utilisateur/*`, `/ats/*`) ; énumérations du schéma redoublées en constantes front.
- Déploiement : Scalingo multi-buildpack, racine `src/web` (`.buildpacks`, `Procfile`, `package.json`, `pnpm-workspace.yaml`) ; le buildpack Node construit le SPA avant `collectstatic`.
- Tests : les e2e de `web` exigent le manifest du build ; `web:test:e2e` dépend de `front:build`.

Seuls deux chemins relatifs (`outDir`, `generate-types`) et l'outillage (mise, workflows, VSCode, docs) dépendent du chemin source. Tous les autres contrats sont avec `web` en tant que service.

## Considered Options

1. Ne rien déplacer, améliorer l'espace de travail VSCode : traite le symptôme.
2. `src/web/frontend` : un niveau de moins, frère des couches Python, déplacement mécanique.
3. `src/web/frontend/ats` : dossier-famille pour des surfaces qui n'existent pas, un niveau conservé.
4. `src/frontend` : sort le SPA de la racine de build Scalingo et du workspace pnpm ; suppose de changer le déploiement.

## Decision

Option 2, en deux étapes.

1. `git mv src/web/presentation/frontend src/web/frontend`, puis repointer `outDir`, `generate-types`, `pnpm-workspace.yaml`, `config_roots` et dépendances mise, filtres de chemins de `web.yml` et `storybook_pages.yml`, `.vscode`, `csplab-frontend.code-workspace`, docs. Django, `bin/sass`, le `build` Scalingo et les tests sont inchangés.
2. Fusionner `csplab-web` et `csplab-frontend` en un seul `package.json` à `src/web` : un `node_modules`, un lockfile, un eslint, plus de workspace ni de `--filter`. Vite reçoit `root: 'frontend'`. Les deux fichiers mise restent : `frontend/mise.toml` garde les tâches `front:*`, exécutées depuis `src/web` via `dir`, pour séparer l'outillage Django de l'outillage Vue.

Principe : `frontend/` contient des sources, `presentation/static/` les artefacts servis. Une seconde surface Vue ou un socle de styles partagé, le jour où ils existent, se placent en frères. L'option 4 devient pertinente si le SPA cesse d'être servi par Django.

## Consequences

- Chemin `src/web/frontend/src/…` ; l'espace de travail frontend n'ouvre que du front.
- Aucun changement de commande : les alias mise `front:*` ne portent pas le chemin.
- Historique conservé par `git mv` ; les branches ouvertes sur le SPA sont à rebaser, à planifier entre deux livraisons.
- Le JS vanilla candidat reste dans `presentation/static` tant qu'il n'a pas de build.
