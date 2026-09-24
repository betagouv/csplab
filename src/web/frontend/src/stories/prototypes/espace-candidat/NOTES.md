# Notes — Prototype espace candidat

Sujet : expérience candidat (découverte d'offre → candidature → suivi), pensée à part de l'ATS
recruteur — pas une simple vue "candidat" du même outil.

## Espace connecté refondu sur la spec « strict nécessaire » (24 septembre 2026)

L'espace connecté du parcours 2 est reconstruit à partir de la spec produit fournie par Alice
(objectifs candidat, accès, liste, détail, conversation, statuts, retrait, compte). Le parcours 1
(candidater sans compte) est inchangé. Les écrans précédents de l'espace connecté (actions à
effectuer, timeline d'étapes, onglet Documents, pastilles d'action) sont supprimés : la spec les
exclut volontairement (« strict nécessaire », le statut candidat ne révèle pas les étapes internes).

### Ce qui est implémenté (stories `Prototypes/Espace candidat mobile`)

- **0B** connexion → espace → déconnexion ; **0C** lien « nouveau message » d'un courriel :
  connexion puis arrivée directe dans la conversation (pile [liste, détail, conversation]).
- Connexion : FranceConnect (bouton mis en avant) ou email + mot de passe ; « Mot de passe
  oublié ? » (envoi d'un lien par courriel, confirmation neutre) ; déconnexion qui mentionne
  aussi FranceConnect quand la session en venait.
- En-tête permanent : logo, pastille des non lus (total des messages non lus), compte. Pas de
  barre de navigation basse.
- Mes candidatures : « En cours » puis « Terminées » repliée ; tri par dernière activité ;
  carte = intitulé, organisme, statut, non lus, dernière activité ; états vides.
- Détail : page unique, dans l'ordre de la spec ; « L'offre » et « Pièces déposées » repliées.
- Conversation : fil ancien → récent, défilement auto, réponse fixée en bas, « Joindre » (photo /
  photothèque / fichiers via de vrais `<input type=file>`, `capture` pour l'appareil photo),
  plusieurs pièces avec aperçu et suppression, formats PDF/DOC/DOCX/ODT/JPG/PNG, échec d'envoi
  avec conservation du contenu et « Réessayer ».
- Retrait : lien réservé aux candidatures en cours, panneau du bas, « Cette action est
  définitive. », motif facultatif ; statut → Retirée, bascule en Terminées, événement au journal
  (`journal` dans l'état, non affiché : c'est côté ATS).
- Mon compte : nom/prénom verrouillés si FranceConnect, mail toujours verrouillé, téléphone
  modifiable, mot de passe modifiable uniquement pour un compte « formulaire ».

Contrôles Storybook sur 0B et les écrans isolés : jeu de données (complet / sans terminées /
vide), mode de connexion, « simuler un échec d'envoi » (première tentative seulement).

### Nouveaux composants (manques du DS)

- **`MobileBottomSheet.vue`** — panneau modal qui monte du bas. Ni `CspDialog` (centré) ni
  `CspDrawer` (gauche/droite) n'ont d'ancre basse. Construit sur Reka Dialog avec les mêmes
  tokens ; piste d'intégration : ajouter `side="bottom"` à `CspDrawer`.
- `EspaceHeader`, `CandidatureListCard`, `StatutCandidatBadge` (badge = `CspBadge`, mêmes
  sémantiques que la doctrine du pipeline recruteur), `RetourLien`.

### Points de la spec à trancher / incohérences relevées

- **Ouvrir une conversation côté candidat** (marqué « à trancher ») : non implémenté, le
  prototype ne permet que de répondre aux fils ouverts par l'équipe.
- **« Retirée » vs « Désistement »** : la table des statuts dit « Désistement », la section
  retrait dit « Retirée ». Le prototype affiche « Retirée » (phrase : « Vous avez retiré cette
  candidature. »).
- **« Offre close » vs « Offre archivée »** : idem, « Offre close » retenu.
- **« Retenue » classée dans Terminées** (spec section 2) alors qu'elle dit « L'équipe vous
  contactera » : une candidature retenue avec message non lu apparaît donc dans Terminées.
- **Liens de création d'espace** : la spec d'accès ne prévoit que la connexion ; le lien
  « Créer mon espace candidat » de la page connexion a été retiré (il reste dans le pop-in de
  succès du parcours 1, non relié à un écran). À confirmer.
- « L'offre, repliée : lieu, type de contrat, catégorie, puis la description » : interprété
  comme un pli fermé qui, ouvert, montre les trois faits puis la description.
- Repostuler après un retrait, et le comportement côté ATS du retrait : « à creuser », non traité.
- Les pièces jointes n'ont ni limite de taille ni antivirus dans le prototype.

## Refonte mobile-first (17 septembre 2026)

Refonte structurelle demandée par Alice : mobile-first, deux parcours strictement indépendants
(candidater sans compte / suivre avec un compte facultatif). Vit dans une nouvelle story
Storybook **`Prototypes/Espace candidat mobile`** (fichier
`EspaceCandidatMobilePrototypes.stories.ts`), avec ses propres composants dans
`variants/mobile/` et `shared/mobile/`. L'itération desktop précédente est conservée telle
quelle sous **`Prototypes/Espace candidat (desktop, itération précédente)`** pour comparaison,
mais n'est plus le fil actif.

### Nouveaux composants mobiles (candidats à l'intégration DS)

- **`MobileTopBar.vue`** — en-tête compact avec flèche retour, remplace `CandidateHeader` dans
  les écrans en pile (offre, candidature, détail).
- **`MobileStepProgress.vue`** — « Étape 2 sur 4 — CV et lettre » + barre de progression fine.
  Remplace le stepper à cercles numérotés (`CandidatureStepper`), illisible sous ~400px.
- **`MobileFlowShell.vue`** — assemble top bar + progression + contenu scrollable + CTA sticky
  plein écran en bas. Remplace `CandidatureFlowShell` pour le parcours sans compte.
- **`MobileFileField.vue`** — zone de dépôt de fichier pensée tactile (gros bouton "Ajouter un
  fichier", puis "Remplacer"/"Supprimer" explicites). Remplace `FileDropzone` (pensé souris/
  drag-and-drop) pour ce parcours.
- **`ConfettiBurst.vue`** — petit effet confettis CSS (pas de librairie ajoutée) pour la pop-in
  de succès festive. Respecte `prefers-reduced-motion`.
- **`FranceConnectButton.vue`** — approximation du bouton FranceConnect (le vrai composant/la
  vraie charte n'existent pas dans ce DS ni ailleurs dans le repo — recherché, rien trouvé).
  À remplacer par le composant officiel si un jour disponible.

Manques DS confirmés par cette refonte : toujours pas de `CspStepper`/`CspTimeline` génériques,
ni de composant d'upload de fichier dans `components/base/`.

### Correction de navigation (retour d'Alice après premier test — écrans depuis remplacés, voir la section du 24 septembre)

Première version de l'espace connecté : barre d'onglets basse à 4 entrées (Candidatures /
Messages / Documents / Profil). Retour d'Alice : il n'y a qu'une seule vraie clé d'entrée,
« Mes candidatures » — Messages et Documents ne sont pas des sections globales, ce sont des
informations *associées à une candidature précise*. Corrigé :

- Plus de barre d'onglets. Navigation en pile (accueil → détail → conversation/documents,
  retour = dépiler), une icône profil dans l'en-tête de l'accueil plutôt qu'un 4ᵉ onglet.
- `ConversationsMobile.vue` et `DocumentsMobile.vue` ne montrent plus une liste globale
  ("toutes mes conversations/documents") : ils prennent un `candidatureId` obligatoire et
  n'affichent que ce qui concerne cette candidature. Ce sont maintenant des écrans qu'on
  atteint uniquement depuis la fiche d'une candidature (ou un raccourci direct depuis une
  action à effectuer, qui cible aussi une candidature précise).
- Le pop-in de succès du parcours 1 dit maintenant « Terminer et retourner sur l'offre »
  (au lieu de « Continuer sans créer de compte ») et ramène effectivement à l'écran offre.

### Décision technique importante : container queries, pas media queries, pour les cartes réutilisées

`ActionRequiseCard.vue` (bouton qui débordait sur mobile) utilise maintenant
`container-type: inline-size` + `@container` plutôt que `@media (min-width: …)`. Raison : cette
carte est réutilisée à l'intérieur d'un conteneur de largeur fixe (colonne mobile de ~390px,
y compris quand elle est affichée sur un écran desktop large). Une media query réagit à la
largeur de la *fenêtre*, pas à celle du conteneur parent — elle se serait déclenchée à tort sur
grand écran alors que la carte reste étroite. Réflexe à garder pour tout composant partagé
entre un contexte pleine largeur et un contexte colonne étroite.

### Données

Les 4 candidatures mock couvrent exactement les 4 états demandés : envoyée sans action
(Instructeur·rice, Préfecture de la Gironde), entretien proposé avec action (Chargé·e de
mission innovation numérique — qui porte aussi la seule demande de document du prototype),
message non lu avec action (Chef·fe de projet SI), en cours d'étude sans action (Responsable
RH). Un « document à fournir » n'est volontairement pas remonté séparément comme action tant
qu'une candidature porte déjà une action prioritaire (éviter 2 pastilles concurrentes sur la
même carte) — reste visible et actionnable dès qu'on ouvre l'onglet Documents.

Une offre externe (`offreExterne`, Conseil régional de Bretagne) a été ajoutée pour tester le
cas "redirection vers un site partenaire" du CTA de la page offre.

## Composants créés pour ce prototype (candidats à l'intégration)

Aucun composant `Csp*` existant ne couvrait ces besoins. Fragments montés dans `shared/`,
à discuter pour une éventuelle promotion en composants `Csp*` du design system :

- **`CandidatureStepper.vue`** — stepper horizontal numéroté (info bulle courante, coche sur
  les étapes faites). Réutilisable pour tout parcours multi-étapes candidat. Manque côté DS :
  `CspStepper`.
- **`EtapesTimeline.vue`** — timeline verticale (fait / en cours / à venir) pour le détail d'une
  candidature. Manque côté DS : `CspTimeline`, avec un statut à 3 valeurs générique.
- **`EtapesResume.vue`** — version compacte horizontale de la même donnée (chevrons), utilisée
  sur les cartes du tableau de bord. Partage le type `EtapeTimeline` avec la timeline verticale.
- **`ActionRequiseCard.vue`** — carte d'alerte "Action requise" avec icône, libellé et CTA.
  Proche d'un `CspCallout` mais avec une mise en page carte + bouton ; à voir si on étend
  `CspCallout` (slot d'action) plutôt que de garder un composant séparé.
- **`FileDropzone.vue`** — zone de dépôt de fichier (drag & drop + sélection), état "fichier
  déposé" avec retrait. Manque côté DS : `CspFileUpload`.
- **`CandidateHeader.vue`** — en-tête public/connecté, volontairement différent de
  `CspAppShell` (pas de sidebar) : l'espace candidat doit se sentir plus léger qu'un outil
  interne. Décision UX, pas une lacune du DS.
- **`CandidatureStepper.vue` + `CandidatureFlowShell.vue`** — le shell factorise l'en-tête, le
  stepper et les boutons Retour/Continuer communs aux 3 parcours de candidature.
- **`CandidatureCard.vue`** — carte de candidature du tableau de bord (poste, organisme, badge de
  phase, résumé d'étapes, prochaine échéance). Combine `EtapesResume` et `CspBadge`.

## Note technique

Les données mock mutées par l'interaction (messages lus, document déposé, action traitée) sont
enveloppées dans `reactive()` (`data/candidatMock.ts`) — un tableau JS "plat" ne déclenche pas
les recomputations Vue quand on mute ses éléments. Sans ça, le badge de messages non lus et le
statut des documents ne se mettaient pas à jour après une action candidat.

## Décisions UX prises pendant le prototypage

- Page offre : un seul mode de candidature traité ("Postuler" ouvre la candidature dans
  l'outil) — la redirection vers un site partenaire a été écartée du périmètre de cette
  session à la demande d'Alice, à retraiter plus tard si besoin.
- Les 3 parcours de candidature (CV / Compte / Formulaire) partagent le même `CandidatureStepper`
  pour rester comparables.
- **Pivot** : Alice a ensuite demandé une piste alternative avec une modalité unique de
  candidature (`variants/candidature-unique/CandidatureUnique.vue`) : un seul formulaire en
  4 étapes (informations, pièces jointes CV + lettre de motivation facultative, questions,
  récapitulatif), confirmation en pop-in plutôt qu'en écran plein. Les deux approches
  coexistent comme stories comparables (« 0. Scénario principal » = modalité unique,
  « 0bis. Variante » = choix entre 3 modes) — à trancher avec l'équipe.
- Le pop-in de succès réutilise directement `CspDialog` du design system, sans aucun
  composant supplémentaire à créer — bon signal que le DS couvre déjà ce besoin.

## Limite connue du prototype

Storybook isole chaque écran dans sa propre story : sans montage explicite d'un composant
« parcours » (comme `ParcoursComplet.vue` / `ParcoursCandidatureUnique.vue`), cliquer sur un
CTA ne mène nulle part. Les stories `0.` et `0bis.` existent précisément pour offrir un
parcours cliquable de bout en bout ; les autres stories restent des écrans isolés, utiles
pour comparer des variantes mais pas pour tester un enchaînement.

## Suite proposée

- Décision d'équipe sur la promotion des composants ci-dessus dans `components/base/`.
- Si le sujet "site partenaire" revient, prévoir une session dédiée à l'ambiguïté du CTA
  "Postuler" (interne vs externe).
- Trancher entre les deux approches de candidature (modalité unique vs choix entre 3 modes)
  avant d'aller plus loin sur ce point précis.
