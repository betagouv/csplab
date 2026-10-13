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

## API publique `/api/v1`

Les champs, les filtres et les valeurs de l'API publique sont en français, y compris les mots traduits ailleurs dans le code (`statut`, `titre`, `profil`). Les sérialiseurs exposent ces noms avec `source=` : le domaine et les cas d'usage gardent leurs noms. Les vues `recruteur` et `identite`, `/api/token`, `/api/fake-ts/` et le schéma d'API interne suivent la règle générale.

- On écrit en snake_case, sans accent : `conditions_exercice`, `mises_a_jour`.
- Un champ porte le même nom en entrée et en sortie, et d'une route à l'autre. On reprend les noms d'entrée de `POST /api/v1/offres/creer_modifier`.
- Le nom vient avant son complément : `url_offre`, `nature_offre`, `type_contrat`, `titre_long`.
- Une date porte le nom de l'événement qu'elle marque : `debut_publication`, `debut_contrat`, `fin_candidature`, `date_archivage`.
- On accorde avec la ressource : `creees` et `mises_a_jour` pour des offres, valeurs `creee` et `mise_a_jour`. Un champ à une seule valeur reste au singulier : `categorie`.
- Les erreurs écrites par nos vues ont la forme `{"erreur": "…"}`, et les upserts renvoient `erreurs[].erreur`.

On garde tels quels :

- l'enveloppe de pagination de DRF (`count`, `next`, `previous`, `results`) et les erreurs que génèrent DRF et simplejwt (`detail`) : les franciser sur `/api/v1` seulement mélangerait deux formats ;
- les messages de validation par nom de champ ;
- les noms que les partenaires emploient déjà et qui se lisent dans les deux langues : `reference`, `source_id`, la valeur `ok` ;
- un champ d'un sérialiseur partagé avec l'entrée, comme `localisation.localisation_label`.

On ne garde pas d'alias pour l'ancien nom : on inscrit le renommage dans les changements non rétrocompatibles de `changelog_api.md`, on met à jour `guide_api.md` et on prévient les partenaires.

## Termes traduits

- équipe → `team`, membre → `member`
- assignation → `assignment`, refus → `rejection`, motif de refus → `rejection_reason`
- activité → `activity`, historique → `history`, tâche → `task`
- paramètres → `settings`, gestion → `management`, liste → `list`
- statut → `status`, intitulé → `title`, nom → `name`, prénom → `first_name`, profil → `profile`
- utilisateur → `user`, espace → `space`
- introuvable, inexistant → `NotFound`
