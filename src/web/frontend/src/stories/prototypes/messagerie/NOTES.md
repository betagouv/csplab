# Notes, proto/messagerie

Prototype Storybook de la messagerie entre l'équipe de recrutement et le candidat : l'onglet Messages du panneau de candidature, et la page de la candidature dans l'espace candidat. Il compare trois présentations du fil sur un même scénario fictif, pour arbitrer le critère « équipe à droite, candidat à gauche » de #1463. Les données sont gardées en mémoire dans la page : recharger la story remet tout à zéro.

## Stories

- `Prototypes/Messagerie/Recruteur` : bulles, pile de messages, correspondance, dans le panneau aux largeurs réelles. Un contrôle choisit la conversation ouverte ; les variantes « sur Pièces complémentaires » servent aux diapositives de pistes du deck.
- `Prototypes/Messagerie/Candidate` : les mêmes présentations dans la page de la candidature, sur ordinateur et sur téléphone.
- `Prototypes/Messagerie/Échange structuré` : la candidate choisit un créneau dans le message, sur la page ou dans un cadre de téléphone ; l'équipe voit le choix attendu puis le créneau retenu.
- `Prototypes/Messagerie/Comparaison` : des fils côte à côte, à la largeur du fil dans le panneau livré sur un écran de 1440 px : les trois présentations, le côté des bulles, immédiat ou différé, le choix du créneau vu par l'équipe. Ces stories ont une hauteur fixe et servent au deck Vignettes `messagerie-prototype`.

Les stories candidate « ouverte sur le dernier message » et « ouverte sur la demande » font défiler la page jusqu'au message, comme une arrivée depuis le courriel de notification.

Les contrôles règlent la présentation, la règle de côté des bulles (équipe à droite ou moi à droite), les indices d'immédiateté (préréglage immédiat ou différé, puis zone de saisie, dates, accusé de lecture, ligne d'attente), l'ordre, l'avancement côté candidat, le délai indicatif, le point de vue et la largeur du panneau.

## Scénario

Candidature de Camille Dupont au poste de chargé·e de communication, envoyée le 1er septembre 2026. Trois agents : Jean-Marc Chateau (responsable), Sophie Nguyen (recruteuse, gestionnaire RH), Karim Benali (contributeur, membre du jury, qui n'écrit dans aucune conversation). Deux conversations : « Pièces complémentaires » du 3 au 15 septembre, avec une relance au bout de cinq jours, et « Organisation de l'entretien » du 22 au 23 septembre, qui se termine sur une question de la candidate restée sans réponse. L'horloge du prototype est fixée au vendredi 25 septembre 2026 à 16 h.

## Mesures

Caractères par ligne, mesurés dans le navigateur sur les paragraphes de plus de 120 caractères, avec le texte à 14 px de l'application.

- Panneau livré sur un écran de 1440 px (panneau de 864 px, fil de 485 px) : bulles 47 à 52, pile 52 à 53, correspondance 58 à 60.
- Panneau de la maquette (1 110 px) : bulles 73 à 77, pile 85 à 91, correspondance 64 à 69.
- Maquette Figma d'origine : 94 caractères dans la pile, une soixantaine dans une bulle.

La plage recommandée va de 50 à 75 caractères, et le critère WCAG 1.4.8 fixe 80 au plus. La correspondance limite son texte à 28rem ; la pile suit la maquette, sans limite.

## Écarts avec les maquettes et les US

- Onglets : seul l'onglet Messages a un contenu. La colonne de droite du panneau (note) est absente de l'onglet Messages, comme sur les maquettes.
- Éditeur : barre d'outils de #1418 (gras, italique, listes, citation), sans effet sur le texte. Les boutons « Pièce jointe » et « Nouvelle conversation » sont inactifs.
- Rôle affiché : côté recruteur, le rôle sur le recrutement ; côté candidat, la fonction de l'agent (« Gestionnaire RH »), plus parlante pour une personne extérieure.
- Lecture : ouvrir une conversation la marque comme lue au bout de 1,5 seconde, pour laisser voir la pastille. Répondre la marque comme lue aussitôt.
- Côté candidat, le réglage « Accusé de lecture » affiche « Lu » sous ses propres messages ; l'avancement affiche « Transmis à l'équipe de recrutement » sous chaque message envoyé.
- Bulles : 80 % de la largeur du fil, pleine largeur sous 26rem, comme Démarche Numérique. Les blocs ont des angles droits.

## Composants à envisager

- Messagerie : ni le DSFR ni la bibliothèque `Csp*` n'ont de fil, de message, de zone de réponse ou de pastille de non-lu. Le prototype les construit dans `thread/`.
- `CspTabs` : pas de pastille sur un onglet, que #1468 demande sur l'onglet Messages.
- `CspTextarea` : un éditeur composé demande une variante sans bordure ; le prototype surcharge l'ombre et le contour de focus.
- Pastille de non-lu : un cercle, seul arrondi posé par le prototype, à valider comme cas particulier.
- Messages repliés de la correspondance : le nom accessible du bouton inclut le début du message, long à l'écoute ; à vérifier au lecteur d'écran.

## Données attendues de l'interface

L'interface de lecture en revue (#1523, PR #1537) renvoie pour chaque message le contenu, le nom de l'auteur, la date et les documents. Chaque présentation du prototype demande en plus :

- le type d'auteur (agent ou candidat) et son identifiant, pour placer les messages et afficher « (vous) » ;
- le rôle ou la fonction de l'agent ;
- la date de lecture par le candidat, pour « Lu à » ;
- la lecture par membre de l'équipe, pour les pastilles ;
- pour la ligne d'attente, le fait qu'un message de l'équipe attend une réponse ;
- pour l'échange structuré, les créneaux, l'échéance et le créneau choisi.
