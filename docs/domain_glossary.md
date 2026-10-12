# Glossaire métier

On écrit les identifiants en anglais, sauf les termes de la section « Termes gardés en français » ([ADR-011](ADR/ADR-011-identifier-language.md)). Quand on introduit un nouveau terme français dans un identifiant, on l'ajoute ici.

## Ajouter un terme

On ajoute un terme quand on répond oui aux trois questions :

1. Les recruteurs, les candidats ou la DGAFP emploient-ils ce mot tel quel, dans un écran, une offre ou un texte statutaire ?
2. Le mot désigne-t-il une chose du service : une entité, un rôle, une notion statutaire ? On traduit les verbes, les adjectifs, les éléments d'interface et les noms génériques comme liste, page, carte, titre ou erreur.
3. La traduction ferait-elle perdre le sens que le service donne au mot ?

## Écrire un terme

On écrit le terme sans accent et on l'associe à des mots anglais : `CandidatureCard`, `onOrganismeSelect`, `RecrutementNotFound`, `useAssignResponsable`. Côté front, on reprend les noms de champs du schéma d'API interne.

## Termes gardés en français

- `candidature` : dossier qu'un candidat dépose sur une offre. On n'écrit pas `application`, qui désigne aussi la couche `application/`.
- `candidat` : personne qui dépose une candidature.
- `offre` : annonce d'emploi publiée sur Choisir le service public.
- `recrutement` : processus d'un organisme pour une offre, avec ses étapes, ses candidatures et son équipe.
- `etape` : étape d'un recrutement où se trouve une candidature.
- `organisme` : employeur public qui recrute.
- `agent` : agent public d'un organisme qui utilise l'ATS.
- `superviseur`, `responsable`, `recruteur`, `contributeur` : rôles d'un agent. `recruteur` désigne aussi l'espace des agents.
- `versant` : fonction publique d'État, territoriale ou hospitalière.
- `categorie` : catégorie statutaire A, B ou C.
- `corps`, `grade`, `concours`, `metier`, `domaineFonctionnel`, `referentiel` : notions statutaires et nomenclatures de la fonction publique.
- `siret` : identifiant d'un établissement au répertoire SIRENE.

Dans le code, on abrège le nom du service en `csp`.

## Termes traduits

- équipe → `team`, membre → `member`
- assignation → `assignment`, refus → `rejection`, motif de refus → `rejection_reason`
- activité → `activity`, historique → `history`, tâche → `task`
- paramètres → `settings`, gestion → `management`, liste → `list`
- statut → `status`, intitulé → `title`, nom → `name`, prénom → `first_name`, profil → `profile`
- utilisateur → `user`, espace → `space`
- introuvable, inexistant → `NotFound`
