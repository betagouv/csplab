# ADR-011 : Langue des identifiants

**Status:** Proposé
**Date:** 2026.10.12
**Deciders:** Lucas P
**Tags:** conventions, naming, frontend, backend

---

## Context

Aucun document ne fixe la langue des identifiants, et le code nomme souvent une même chose de deux façons : `categorie` et `category`, `offre` et `offer`, `versant` et `Verse`, `formatCandidatNom` et `formatCandidatName`. Le lecteur doit vérifier qu'il s'agit de la même chose, et une recherche sur l'un des noms manque une partie des usages.

Certains mots n'ont pas d'équivalent anglais fidèle : `corps`, `grade`, `versant` sont des notions statutaires, `candidature` ou `etape` sont les mots des écrans et des recruteurs.

## Considered Options

1. Tout en français : on mélangerait les deux langues dans chaque composant, à cause des noms du framework et des composants d'interface (`props`, `Dialog`, `Drawer`).
2. Tout en anglais : on perdrait les mots des recruteurs et de la DGAFP, et on traduirait mal les notions statutaires.
3. L'anglais, sauf pour les termes d'un glossaire métier.

## Decision

On écrit les identifiants en anglais, sauf les termes gardés en français que liste [`docs/domain_glossary.md`](../domain_glossary.md). L'auteur d'une PR qui introduit un nouveau terme français l'ajoute au glossaire.

Les textes affichés, les ADR et les messages de commit restent en français. Les champs, les filtres et les valeurs de l'API publique `/api/v1`, que des partenaires appellent, sont aussi en français : le glossaire en fixe les règles.

## Consequences

On applique la règle au code neuf ou modifié, et on renomme l'existant en quatre PR :

1. les doublons de termes ;
2. les cas d'usage, les erreurs et les méthodes des entités ;
3. les événements, avec une migration de données : leur nom est stocké dans `audit_logs.event_name`, et le front l'emploie comme clé des libellés de l'historique ;
4. les champs des modèles, avec le schéma d'API interne et les types du front.

## Open Questions

- Le glossaire retient `offre`, employé par le contexte `recruteur`, le front et les chemins de l'API publique. L'ingestion, le référentiel et la table `offers` emploient `offer` : faut-il les renommer ?
- Le glossaire réserve `categorie` à la catégorie statutaire. Pour la catégorie d'une étape, on propose de traduire le mot et de renommer `CategorieEtapeRecrutement` en `EtapeCategory`, dans la PR des doublons.
- Le glossaire traduit motif de refus en `rejection_reason`. On propose de renommer `motif_refus` dans la PR des champs, avec le schéma d'API interne.
- Le glossaire retient `candidat`, alors que le contexte back s'appelle `candidate`. Son renommage touche l'adresse `/candidate/` et le label de l'app Django : faut-il le faire ?
