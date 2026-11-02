# ADR-011 : Langue des identifiants

**Statut:** Proposé
**Date:** 2026.10.12
**Decideurs:** Lucas P
**Tags:** conventions, naming, frontend, backend

---

## Contexte

Aucun document ne fixe la langue des identifiants, et le code nomme souvent une même chose de deux façons : `categorie` et `category`, `offre` et `offer`, `versant` et `Verse`, `formatCandidatNom` et `formatCandidatName`. Le lecteur doit vérifier qu'il s'agit de la même chose, et une recherche sur l'un des noms manque une partie des usages.

Certains mots n'ont pas d'équivalent anglais fidèle : `corps`, `grade`, `versant` sont des notions statutaires, `candidature` ou `etape` sont les mots des écrans et des recruteurs.

## Options Considérées

1. Tout en français : on mélangerait les deux langues dans chaque composant, à cause des noms du framework et des composants d'interface (`props`, `Dialog`, `Drawer`).
2. Tout en anglais : on perdrait les mots des recruteurs et de la DGAFP, et on traduirait mal les notions statutaires.
3. L'anglais, sauf pour les termes d'un glossaire métier.

## Décision

On écrit les identifiants en anglais, sauf les termes gardés en français que liste [`docs/domain_glossary.md`](../domain_glossary.md). L'auteur d'une PR qui introduit un nouveau terme français l'ajoute au glossaire.

Les textes affichés, les ADR, les titres de PR et les messages de commit sont en français. On ne renomme pas l'API publique `/api/v1`, que des systèmes externes appellent. Ses champs, ses filtres et ses valeurs sont en français, et le glossaire fixe les règles des noms qu'on y ajoute.

## Conséquences

On applique la règle au code neuf ou modifié, et on renomme l'existant en quatre PR :

1. les doublons de termes ;
2. les cas d'usage, les erreurs et les méthodes des entités ;
3. les événements, avec une migration de données : leur nom est stocké dans `audit_logs.event_name`, et le front l'emploie comme clé des libellés de l'historique ;
4. les champs des modèles, avec le schéma d'API interne et les types du front.

Deux renommages demandent un chantier à part :

- `offer` en `offre` dans l'ingestion, le référentiel et la table `offers` : on le fait dans une PR dédiée, à cause de la migration de cette table.
- le contexte `candidate` en `candidat` : on le fait à la reprise de l'espace candidat, soit en convertissant d'abord l'app selon l'[ADR-009](ADR-009-idiomatic-django-switch.md), soit en créant une nouvelle app qui remplace `candidate`.

## Questions Ouvertes

- Le glossaire réserve `categorie` à la catégorie statutaire. Pour la catégorie d'une étape, on propose de traduire le mot et de renommer `CategorieEtapeRecrutement` en `EtapeCategory`, dans la PR des doublons.
- Le glossaire traduit motif de refus en `rejection_reason`. On propose de renommer `motif_refus` dans la PR des champs, avec le schéma d'API interne.
