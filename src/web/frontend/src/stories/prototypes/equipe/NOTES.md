# Prototype « Équipe de recrutement »

Expérience cible des issues #931, #1053, #934, #935, #936 et #937 (epic « Rôles & permissions »), avec les tickets front #1116, #1117, #1118, #1120 à #1123, #1142 et #1143. Le prototype vit dans Storybook, sans appel réseau : l'état est en mémoire et se réinitialise au rechargement de la story.

## Périmètre

- Liste des recrutements avec attribution d'un responsable, unitaire ou en lot.
- Paramètres d'un recrutement : équipe (ajout, changement de rôle, retrait), invitation à la volée, fil d'activité.
- Paramètres de l'organisme : membres (création de compte, changement de rôle, révocation), journal d'audit.
- État vide de l'agent rattaché à aucun recrutement.
- Sélecteur de point de vue (Gestionnaire, Responsable, Recruteur, Agent sans offre, Admin) qui rejoue chaque écran avec les droits du rôle.

## Règles appliquées

| Action | Admin | Gestionnaire | Responsable de l'offre | Recruteur / Contributeur | Agent sans offre |
|---|---|---|---|---|---|
| Voir la liste des recrutements | Tous | Tous | Ses offres | Ses offres | État vide |
| Assigner un responsable | Oui | Oui | Non | Non | Non |
| Ajouter, retirer, changer le rôle d'un recruteur ou contributeur | Oui | Oui | Oui | Non | Non |
| Inviter une personne sans compte depuis une offre | Oui | Oui | Oui | Non | Non |
| Paramètres de l'organisme | Oui | Oui | Non | Non | Non |
| Promouvoir un membre gestionnaire | Oui | Non | Non | Non | Non |
| Révoquer un membre de l'organisme | Oui | Oui | Non | Non | Non |

Les issues laissent deux points ouverts que le prototype tranche :

- Le gestionnaire peut modifier une équipe de recrutement sans être responsable de l'offre (#935 ne parle que du responsable). Le prototype l'autorise : il désigne les responsables, il lui semble incohérent de ne pas pouvoir corriger une équipe.
- Un membre ne peut pas modifier son propre rôle ni se révoquer au niveau organisme : la ligne n'a pas de menu d'actions.

## Choix d'interaction

- **Un seul tiroir « Ajouter un membre »** dans trois contextes (#1118) : équipe d'une offre, attribution unitaire depuis la colonne Responsable ou le menu d'une ligne, attribution en lot depuis la sélection. Le contexte fixe le rôle (responsable) ou le laisse choisir (recruteur, contributeur).
- **Recherche par nom ou courriel** avec suggestions parmi les membres de l'organisme. Un courriel inconnu fait apparaître l'action « Inviter … », qui ouvre le mini-formulaire (#936). Un courriel connu mais déjà dans l'équipe l'indique sans proposer d'invitation.
- **Attribution en lot** (#934) : les cases à cocher n'apparaissent qu'aux rôles autorisés. La barre de sélection remplace la barre d'outils. Le compteur « N sans responsable » filtre la liste et disparaît quand toutes les offres ont un responsable.
- **Traçabilité** : chaque action alimente l'onglet Activité de l'offre ou le journal d'audit de l'organisme, avec un message de confirmation.
- **Invitation en attente** : un compte créé à la volée porte un badge jusqu'à sa première connexion (#991) et propose « Renvoyer l'invitation » dans son menu (#1142, #1143).
- **Promotion en gestionnaire** : l'entrée de menu reste visible mais désactivée pour un gestionnaire, avec la mention « administrateur uniquement », pour que la règle soit lisible sans être contournable.

## Écarts avec les maquettes

- Les maquettes affichent les responsables sous forme de badges d'initiales. Le prototype affiche les noms complets, comme la page Recrutements actuelle.
- Le bouton « Ajouter un membre » se trouve dans la barre d'outils du tableau, comme sur la page des membres de l'organisme, et non à droite du titre de section.
- Les onglets « Étapes de recrutement » renvoient au paramétrage existant de l'application et ne sont pas rejoués ici.

## Évolutions de composants à envisager

- `CspCombobox` : une action « Inviter … » quand la recherche ne trouve rien existe déjà (`actionLabel`) ; il manque un état « déjà membre » distinct de l'état vide.
- `CspDropdownMenu` : une description ou un motif sur un élément désactivé éviterait de l'écrire dans le libellé.
- `CspTableToolbar` : le libellé de sélection (« N sélectionnés ») gagnerait à accepter le nom de l'objet (« N offres sélectionnées »).
- `CspTag` dismissible : la variante pleine est lourde pour une liste d'offres sélectionnées ; une variante claire serait plus lisible.

## Données absentes du modèle

- La fonction dans le recrutement (tag métier) est une liste fixe en attendant le module tags (#935).
- La date de dernière activité par agent et le statut d'activation (#991, #994) n'existent pas encore côté API.
