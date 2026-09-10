# Notes — Prototype espace candidat

Sujet : expérience candidat (découverte d'offre → candidature → suivi), pensée à part de l'ATS
recruteur — pas une simple vue "candidat" du même outil.

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

## Décisions UX prises pendant le prototypage

- Page offre : un seul mode de candidature traité ("Postuler" ouvre la candidature dans
  l'outil) — la redirection vers un site partenaire a été écartée du périmètre de cette
  session à la demande d'Alice, à retraiter plus tard si besoin.
- Les 3 parcours de candidature (CV / Compte / Formulaire) partagent le même `CandidatureStepper`
  pour rester comparables.

## Suite proposée

- Décision d'équipe sur la promotion des composants ci-dessus dans `components/base/`.
- Si le sujet "site partenaire" revient, prévoir une session dédiée à l'ambiguïté du CTA
  "Postuler" (interne vs externe).
