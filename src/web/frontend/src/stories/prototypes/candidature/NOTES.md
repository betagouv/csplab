# Notes — proto/panneau-candidature

Prototype Storybook autonome du panneau de candidature (epic « Consultation d'une candidature »).
Les données sont fictives et vivent dans la page ; recharger la story remet tout à zéro.

## Écarts entre les maquettes lofi et les critères d'acceptation

Quand les deux divergent, le prototype suit les critères d'acceptation des issues, plus récents.

- **Garde-fou (#1006)** : la maquette titre « Quitter sans sauvegarder ? » avec le bouton principal
  sur « Quitter sans enregistrer ». L'issue impose « Modifications non enregistrées », le texte
  « Si vous quittez maintenant, votre saisie sera perdue », le bouton principal « Continuer
  l'édition » et le secondaire « Quitter sans enregistrer ». Le prototype suit l'issue.
- **Accès refusé (#1152)** : la maquette affiche l'intitulé de l'offre en titre de page et dans
  le fil d'Ariane. L'issue interdit toute information du dossier, offre comprise. Le prototype
  titre « Candidature ».
- **En-tête (#1007 / #1329)** : localisation et téléphone n'ont aucune source dans le modèle
  aujourd'hui. Le prototype les affiche quand la donnée fictive existe et n'affiche rien sinon,
  pour valider le comportement « une information absente n'affiche rien ».

## Choix d'interaction à valider

- **Changer d'étape** : la maquette montre un menu déroulant sous le bouton, l'issue #1328 prévoit
  de réutiliser le tiroir de changement d'étape du kanban. Le prototype suit la maquette (menu).
- **Après un changement d'étape**, le panneau passe à la candidature qui suivait dans la colonne
  d'origine, et se ferme s'il n'y en a pas. Le compteur passe par exemple de 1/4 à 1/3.
- **Message de confirmation** : un seul à la fois, 10 secondes, avec le lien « Revenir à cette
  candidature » qui rouvre la candidature dans sa nouvelle colonne.
- **Colonne de droite** hors des onglets : une note en cours reste là quand on change d'onglet.
  L'onglet Notes partage le même brouillon.
- **Tags** : ajout depuis la liste de l'organisme (recherche, « Déjà ajouté » grisé), retrait au
  clic sur la croix. Un sélecteur ouvert compte comme une saisie en cours pour le garde-fou.
- **Clavier** : les flèches gauche et droite passent à la candidature précédente ou suivante
  quand le focus est hors d'un champ de saisie. Échap ferme le panneau.
- **Panneau non modal** : le kanban reste visible et cliquable, sans voile. La maquette montre le
  kanban en clair derrière le panneau ; un voile aurait masqué le contexte que le panneau doit
  préserver.

## Ossature du panneau

Le panneau reprend l'ossature de page de DDR-002 à l'intérieur du tiroir : un en-tête pleine
largeur (retour, avatar, nom et étiquette d'étape, intitulé de l'offre, métadonnées `CspMetaList`
comme sous-titre, actions à droite), une barre d'onglets qui borde toute la largeur de la colonne
principale et reste collée en haut au défilement, un contenu aligné sur la gouttière du tiroir, et
une barre de navigation en pied. La colonne de droite est une région distincte sur toute la
hauteur, fond alternatif et bordure gauche, avec son propre défilement ; elle passe sous le contenu
principal quand la largeur manque (DDR-005). Les états vide et d'exception du CV reprennent
`CspEmptyState` (DDR-006).

## Composants du design system : évolutions à envisager

- **`CspDrawer`** : le panneau a besoin d'une largeur « tout sauf une colonne de kanban », d'un
  corps sans padding pour poser la barre d'onglets et la colonne de droite bord à bord, et d'un
  en-tête sans bordure basse quand une barre d'onglets suit. Le prototype force
  `--base-drawer-width` en style inline et surcharge les paddings en CSS global ; une variante
  `panel` du tiroir (largeur, corps nu, en-tête composable) porterait ces besoins proprement.
- **`CspToast`** : l'action est placée à droite du texte et compresse le titre dans un toast à
  deux lignes. La maquette place le lien sous la description. Le prototype passe le lien dans le
  slot par défaut ; une prop `actionPlacement` ou un slot dédié sous le texte serait utile.
- **`CspDropdownMenu`** : pas de moyen de marquer l'élément courant autrement qu'en le
  désactivant. Le prototype ajoute « (étape actuelle) » au libellé ; la maquette montre un badge.
- **`CspCard`** : cliquable seulement via `href`. Le prototype pose `role="button"` et
  `tabindex` sur la carte du kanban, comme le proto tableau de bord l'avait fait.
- **`CspTabs`** : les libellés passent à la ligne dans un conteneur étroit ; `white-space: nowrap`
  forcé depuis le panneau.
- **Composant à créer** (#1326) : compteur « Candidature 2 sur 4 » avec Précédent / Suivant.
  `PanelFooter.vue` en est la première forme.

## Données absentes du modèle

- Journal d'activité : `GET /recruteur/candidatures/{uuid}/activites` (#1330).
- Candidature seule : `GET /recruteur/candidatures/{uuid}` (#1323).
- Tags d'organisme et tags de candidature : aucun endpoint.
- Note privée : le modèle `Note` n'a pas de visibilité.
- CV et documents : stockage à venir (#543).
