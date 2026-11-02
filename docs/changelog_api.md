# Changelog de l'API publique

Le changelog de l'API publique (`/api/v1/…`, `/api/fake-ts/…`) est affiché dans Redoc,
dans la section « Changelog » de `/api/schema/redoc`. Il est assemblé à partir d'un
fichier par changement, dans `src/web/presentation/static/api/changelog_api.d/`.

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
  `AAAA-MM-JJ`, `pr` entier, `liens` sous forme d'URL, corps non vide ;
- sur la PR, pour les fragments ajoutés : refuse une date dans le futur, ou un `pr`
  différent du numéro de la PR, et avertit si la date a plus de 3 jours ;
- dans la merge queue, pour les fragments ajoutés : refuse une date qui n'est pas
  comprise entre aujourd'hui − 3 jours et aujourd'hui.

Une PR qui porte le label `changelog-api-migration` n'est vérifiée que sur le format,
pour reprendre des fragments avec leur date déjà publiée.

En local : `mise run web:lint:changelog-api` (format seul), ou
`mise run web:lint:changelog-api -- --base origin/main --pr <numéro>`.

## Assemblage

`schema.yaml` garde le tag `changelog` sans description : son contenu n'y est pas
recopié, et deux PR n'y entrent pas en conflit. Redoc charge `/api/schema/public`, qui
sert `schema.yaml` avec la description de ce tag assemblée à partir des fragments :
par date décroissante, puis par type (non rétrocompatible, ajouté, modifié, corrigé,
retiré), puis par numéro de PR. Le résultat est gardé en mémoire jusqu'au déploiement
suivant.
