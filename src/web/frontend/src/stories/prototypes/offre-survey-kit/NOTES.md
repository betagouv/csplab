# Offre survey-kit — formulaire décrit en données (piste 2)

Proto du 26/11/2026, branche `proto/offre-survey-kit` (partie de `proto/creation-offre`).
Lucas a proposé de tester [survey-kit](https://shallowred.github.io/survey-kit/), son outil pour décrire des formulaires
riches en JSON avec un rendu DSFR. Alice a choisi la **piste 2** : reprendre le principe **sans rien installer**
(aucune modification de `package.json`, du lockfile ni de la config ; composants partagés `Csp*` inchangés).

**Données fictives.** Toutes les listes de choix (familles et métiers RMFP+, compétences, corps et grades, langues,
fondements juridiques…) sont des extraits fictifs repris du proto « Offres sans autorisation (MVP) », pas les
référentiels officiels. Rien n'est enregistré ni publié.

## Stories (`Prototypes/Offre survey-kit`)

1. **Éditeur** : la description JSON à gauche (modifiable), le formulaire produit à droite, les réponses en JSON
   dessous. On modifie la description, le formulaire suit (0,3 s après la frappe). Si la description n'est plus
   valable (JSON cassé, question inconnue, condition illisible…), la liste des problèmes s'affiche et le formulaire
   garde la dernière version valable. Boutons « Rétablir la description d'origine » et « Vider les réponses ».
2. **Créer une offre** : le formulaire seul, dans le même cadre de page que le MVP, à comparer à
   `Prototypes/Offres sans autorisation (MVP) › 2. Créer une offre`.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `offre.formulaire.json` | La description : `reponses` (une entrée par réponse) et `questionnaire` (parties → étapes → pages → questions). |
| `moteur.ts` | Lecture et vérification de la description, conditions d'affichage, choix dépendants, avancement par étape. |
| `ChampDecrit.vue` | Une question → le composant `Csp*` de son type. |
| `FormulaireDecrit.vue` | Le formulaire en étapes (même présentation que `ParcoursOffre` du MVP). |
| `EditeurDescription.vue`, `CreerOffreDecrite.vue` | Les deux stories. |

Réutilisé du MVP par import, sans le modifier : `ChampDate`, `ChoixMultiple`, `ChampSimple`, `TexteEtoile`,
`avancementEtape` (aide.ts), `PageAts` et `nav`, `shared/ListEditor`.

## Le format, en bref

Inspiré du format de survey-kit (étapes, pages, questions, `visibleWhen`), avec des clés en français.

```text
"reponses": {
  "natureEmploi": { "type": "choix", "affichage": "radio", "libelle": "Nature de l'emploi", "obligatoire": true,
                    "choix": [{ "valeur": "titulaire", "libelle": "Fonctionnaires uniquement" }, …] },
  "fondementJuridique": { …, "visibleSi": "natureEmploi = les_deux || natureEmploi = contractuel" },
  "grades": { "type": "choix-multiple", "filtrePar": "corps", "siParentVide": "desactive",
              "choix": [{ "valeur": "Attaché", "parent": "Attachés d'administration de l'État" }, …] },
  "competences": { "type": "choix-multiple", "preRempliPar": { "question": "metier", "donnee": "competences" }, … }
},
"questionnaire": { "parties": [{ "id": "annonce", "titre": "Annonce visible du candidat",
  "etapes": [{ "id": "cadre", "titre": "Le cadre du recrutement",
    "pages": [{ "id": "cadre", "questions": ["natureEmploi", { "id": "statutPoste", "largeur": "demi" }, …] }] }] }] }
```

- **Types** : `texte`, `url`, `nombre`, `texte-long`, `date` (saisie JJ-MM-AAAA, gardée en AAAA-MM-JJ), `choix`
  (liste déroulante, `radio` ou `segments`), `choix-multiple` (recherche + étiquettes), `oui-non`, `interrupteur`,
  `liste-texte` (ajouter / retirer des lignes), `repetable` (ex. langue + niveau).
- **Conditions** (`visibleSi`) : `a = x`, `a != x`, `a > 3`, `a.includes(x)`, `a.excludes(x)`, `a` (rempli), `!a` (vide),
  combinées par `&&` et `||`. Une question masquée ne compte pas dans les obligatoires et n'apparaît pas dans les réponses.
- **Dépendances** : `filtrePar` + `parent` sur chaque choix (Métier filtré par Famille, Corps par Catégorie, Grade par
  les Corps choisis) ; `siParentVide` : tout proposer ou désactiver le champ ; `preRempliPar` (compétences du métier).
  Les dépendances se propagent en cascade : changer la catégorie retire les corps qui ne correspondent plus, puis
  leurs grades ; changer la famille vide le métier, puis ses compétences.
- **Avancement** : par étape, comme le MVP (« 2 champs obligatoires * à remplir », « Étape complétée »…), et le total
  restant en dernière étape (le bouton « Publier » reste grisé tant qu'il en manque).

## Ce que l'approche apporte

- **Le formulaire se lit et se modifie sans toucher au code des écrans** : ajouter un champ, changer un libellé, une
  aide, une liste, rendre un champ obligatoire ou conditionnel = une ligne dans le JSON. L'éditeur permet de l'essayer
  tout de suite.
- **Les règles sont au même endroit que les champs** : conditions d'affichage, champs obligatoires et dépendances
  sont visibles d'un coup d'œil (8 conditions ou dépendances dans ce formulaire), au lieu d'être réparties dans
  `FormAnnonce.vue` (700 lignes), `aide.ts` et `resume.ts`.
- **Une seule source pour plusieurs usages** : la même description pourrait produire le formulaire, le résumé des blocs
  de la page de l'offre, la liste « ce qui manque pour publier » et la validation côté serveur.
- **Le rendu reste celui du kit** (`Csp*`) : pas de second design system à charger.
- **Base de discussion avec Lucas** : le format est proche de celui de survey-kit, la traduction vers son format est
  mécanique pour l'essentiel.

## Limites et écarts avec le formulaire actuel (MVP)

- **Pages = blocs du même écran.** Dans survey-kit, une page est un écran. Ici, pour rester comparable au MVP (une
  étape = un écran), les pages d'une étape s'affichent l'une sous l'autre, avec leur titre.
- **Mise en page simplifiée** : chaque question a une largeur (pleine, moitié, tiers) dans une grille ; on ne peut pas
  forcer un retour à la ligne. Ex. : Catégorie et Corps se retrouvent côte à côte, alors que le MVP les met chacun sur
  sa ligne.
- **Lieux sans géolocalisation** : une simple liste d'adresses (le MVP propose une saisie assistée géolocalisée).
- **Pas d'aide à la rédaction** : les alertes du MVP (sigles, phrases longues, « Mettre en forme ») et le badge « Repris
  de la fiche » ne sont pas décrits. Il faudrait un type de règle « conseil » dans le format.
- **Famille comptée comme obligatoire** : le MVP l'affiche avec un astérisque mais ne la compte pas ; ici elle compte
  (l'étape « Le métier » a 2 champs obligatoires au lieu d'1).
- **« Choix multiple »** : la valeur enregistrée est le libellé (corps, grades, compétences) ; prévoir des codes si
  les référentiels en ont.
- **Conditions sans parenthèses** et sans calcul (ex. « date de fin ≥ date de début + 1 mois ») : à ajouter si besoin,
  ou à reprendre de survey-kit (publicodes).
- **Pas de validation de format** (URL, nombre positif, date valide) ni de messages d'erreur sous les champs.
- **Description lue telle quelle** : le format n'a pas de schéma formel (JSON Schema) ; la vérification de l'éditeur
  couvre les erreurs courantes (question inconnue, type inconnu, condition illisible), pas toutes.
- **Rien n'est conservé** entre deux chargements de la story.

## Pour passer à la vraie lib (piste 1) — nécessite l'accord de Lucas

À installer (refusé dans la piste 2) : `@jsonforms/core` et `@jsonforms/vue` 3.8, `@gouvminint/vue-dsfr` ≥ 8.11
(et le CSS `@gouvfr/dsfr`), `@shallowred/jsonforms-vue-dsfr`. D'après le dépôt de survey-kit (lu le 26/11/2026), les
paquets `@shallowred/*` ne sont **pas encore publiés sur npm** : ils s'installent depuis les archives des versions
GitHub, ce qui est à valider avec Lucas.

Ce qu'il faudrait faire ensuite :
- **Convertir la description** vers le format qu'attend `jsonforms-vue-dsfr` : un JSON Schema (draft 2020-12) pour les
  réponses, un « uischema » de type `Categorization` pour les parties / étapes, des conditions en `if` / `then` /
  `allOf`. Le passage depuis `offre.formulaire.json` peut être un petit script.
- **Ajv 2020** : JSON Forms utilise par défaut Ajv draft-07, il faut passer `createAjv2020()` (indiqué dans le README).
- **Renderers spécifiques** pour ce qui n'existe pas en standard : choix multiple avec recherche + étiquettes, date
  JJ-MM-AAAA, répétable langue + niveau, choix filtrés par une autre réponse, pré-remplissage des compétences.
  JSON Forms permet d'ajouter ses propres renderers (`[...dsfrRenderers, { renderer, tester }]`).
- **Avancement par étape** et « Étape complétée » : à recalculer à partir des erreurs Ajv, ou garder le calcul de
  `moteur.ts`.

## Écarts de rendu attendus vue-dsfr vs `Csp*` — **à vérifier**

Non vérifiés à l'écran : le site de survey-kit n'a pas pu être affiché dans l'outil de lecture utilisé. Points à
regarder si on teste la piste 1 :
- **Listes déroulantes** : vue-dsfr utilise la liste native du navigateur ; `CspSelect` est une liste personnalisée.
- **Choix multiple** : pas d'équivalent direct de `ChoixMultiple` (recherche + étiquettes) dans vue-dsfr, a priori.
- **Date** : vue-dsfr propose le champ date natif (format selon le navigateur), pas la saisie JJ-MM-AAAA du MVP.
- **Interrupteur, radios, segments** : composants DSFR équivalents, mais tailles et espacements à comparer.
- **Styles** : le CSS global du DSFR chargé à côté des jetons `--csp-*` peut changer l'apparence des écrans existants ;
  à isoler.
- **Libellés et astérisques** : le DSFR marque les champs obligatoires différemment du MVP (astérisque rouge).

## Note technique (pour Lucas)

Dans le worktree, `pnpm install` échouait (« SyntaxError: Invalid or unexpected token ») : pnpm 11 (installé par mise)
essaie de lancer avec Node le binaire natif de pnpm 12.9.1 demandé par `packageManager`. Contourné en lançant
directement ce binaire (`~/Library/pnpm/store/v11/links/@/pnpm/12.9.1/…/pnpm install --frozen-lockfile`).
Le même problème touche le dossier principal `~/Projects/csplab` (`pnpm --version` y échoue aussi).
