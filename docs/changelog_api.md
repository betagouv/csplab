# Changelog de l'API publique

Le changelog de l'API publique (`/api/v1/…`, `/api/fake-ts/…`) est assemblé à partir
d'un fichier par changement, dans `src/web/presentation/static/api/changelog_api.d/`.
Il est publié :

| Où | Pour qui |
|---|---|
| `/pages/changelog_api` | Page du site, filtrable, une ancre par changement |
| `/api/changelog.md` | Outils et agents : le changelog en Markdown, liens absolus |
| `/api/changelog.json` | Outils et agents : une entrée par fragment, avec ses routes |
| `/api/changelog.atom` | Flux Atom, une entrée par fragment |
| Section « Changelog » de `/api/schema/redoc` | Intégrateurs, à côté de la référence |

Les trois routes `/api/changelog.*` et la page acceptent les mêmes filtres : `type`
(répétable), `route` (ex. `POST /api/v1/offres/creer_modifier`) et `depuis`
(`AAAA-MM-JJ`). `route` n'accepte qu'une route citée par au moins un fragment. Une
valeur invalide renvoie une erreur `400` sur les routes `/api/…`, et est ignorée, avec
un message, sur la page. Le message liste les valeurs possibles sans recopier la valeur
reçue, pour qu'une URL fabriquée ne puisse pas injecter de texte dans la réponse. `/llms.txt` liste ces documents et le guide
en Markdown (`/api/guide.md`) pour les agents.

Ces trois routes ignorent l'en-tête `Accept` (chacune ne sert qu'un format) et ne sont
pas enregistrées dans `api_logs`, qui suit l'usage de l'API par les partenaires.

Une PR qui change l'API publique n'ajoute que des fichiers dans ce dossier : deux PR ne
peuvent pas entrer en conflit.

## Ajouter un changement

Créez un fichier Markdown au nom libre et descriptif, avec un en-tête YAML :

```markdown
---
type: non_retrocompatible   # non_retrocompatible | ajoute | modifie | corrige | retire
date: 2026-10-27            # date de merge, mise à jour juste avant le merge
pr: 2085                    # numéro de la PR qui ajoute ce fichier
liens:                      # facultatif, ticket(s) concerné(s)
  - https://github.com/betagouv/csplab/issues/2072
---

`POST /api/v1/offres/creer_modifier` : une offre dont […] est désormais rejetée.

### Compatibilité

Renseignez dans `region` […]
```

- `type`, `date` et `pr` sont obligatoires.
- Le corps cite la ou les routes concernées, entre backticks et avec leur méthode :
  `` `POST /api/v1/offres/creer_modifier` ``. Ce sont elles qui alimentent le filtre par
  route. Une route avec paramètre s'écrit comme dans le schéma
  (`` `GET /api/v1/offres/sources/{source_id}` ``) ou avec une valeur
  (`` `GET /api/fake-ts/referentials/department` ``).
- Le nom du fichier sert d'identifiant au changement (ancre de la page, `id` du JSON et
  du flux Atom) : ne renommez pas un fragment publié.
- Un fragment n'a qu'un type. Une PR qui ajoute un champ et en modifie un autre ajoute
  deux fragments.
- Le lien vers la PR (`pr`) et vers les tickets (`liens`) est ajouté à la fin de
  l'entrée.
- Les sous-sections `### Titre` du corps (en général `### Compatibilité`) sont
  affichées en citation juste sous leur entrée, pour rester rattachées au changement
  qu'elles décrivent. Sous une entrée d'une seule puce, la citation est rattachée à
  la puce. Sous une liste de plusieurs puces, elle vient après la liste et vaut pour
  toute l'entrée. Le corps n'accepte pas de titre de niveau `#` ou `##`.

## Dater le fragment avant le merge

Juste avant de mettre la PR dans la merge queue :

```bash
mise run web:changelog-api:dater
```

La tâche met la date du jour (heure de Paris) dans les fragments ajoutés par la branche
depuis `origin/main`. Committez le résultat.

## Vérifications en CI

Le job `changelog-api` du workflow Web :

- valide tous les fragments : extension `.md`, en-tête YAML, `type` connu, `date` au format
  `AAAA-MM-JJ`, `pr` entier, `liens` sous forme d'URL, corps non vide qui cite au moins
  une route ;
- sur la PR, pour les fragments ajoutés : refuse une date dans le futur, un `pr`
  différent du numéro de la PR, ou une route absente de `schema.yaml` (sauf pour le type
  `retire`, dont la route peut avoir disparu), et avertit si la date a plus de 3 jours ;
- dans la merge queue, pour les fragments ajoutés : refuse une date qui n'est pas
  comprise entre aujourd'hui − 3 jours et aujourd'hui.

Le job échoue aussi dès que le changelog compte 300 changements (`PAGE_MAX_FRAGMENTS`).
La page `/pages/changelog_api` les affiche tous, sans pagination : 58 changements pèsent
154 Ko (25 Ko compressés). Au-delà du seuil, il faut la découper, par exemple une page
par année ou des mois repliés. Une fenêtre de temps par défaut casserait les liens
permanents vers les changements plus anciens.

Une PR qui porte le label `changelog-api-migration` n'est vérifiée que sur le format,
pour reprendre des fragments avec leur date déjà publiée. Le format comprend la citation
d'au moins une route : un fragment repris sans route ferait échouer `main` ensuite.

En local : `mise run web:lint:changelog-api` (format seul), ou
`mise run web:lint:changelog-api -- --base origin/main --pr <numéro>`.

## Assemblage

`schema.yaml` garde le tag `changelog` sans description : son contenu n'y est pas
recopié, et deux PR n'y entrent pas en conflit. Redoc charge `/api/schema/public`, qui
sert `schema.yaml` avec la description de ce tag assemblée à partir des fragments :
par date décroissante, puis par type (non rétrocompatible, ajouté, modifié, corrigé,
retiré), puis par numéro de PR. La page et les routes `/api/changelog.*` suivent le même
ordre. Les fragments, leur rendu HTML et le guide sont lus une fois et gardés en
mémoire jusqu'au déploiement suivant.

Les routes `/api/changelog.*` et `/api/guide.md` sont documentées dans Redoc, sous
« Changelog et documentation ». Elles sont publiques, sans authentification, et limitées
à 60 appels par minute et par adresse IP (`DocumentationRateThrottle`, taux
`documentation`), que l'appelant envoie ou non un en-tête `Authorization`.
