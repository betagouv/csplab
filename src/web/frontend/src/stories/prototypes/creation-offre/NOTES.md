# Notes — Prototype création d'offre

Sujet : transformer un besoin de recrutement en offre prête à être validée puis publiée, dans le
futur ATS de la fonction publique. Le parcours est pensé comme une étape du recrutement (besoin → offre
→ validation → diffusion → suivi des candidatures), pas comme un formulaire de publication.

Stories : `Prototypes/Création d'offre`. Un seul parcours, ouvert dans six états :

| Story | Point d'entrée | Ce qu'elle montre |
| --- | --- | --- |
| 0. Scénario complet | Écran de démarrage | Choix de la source, aperçu « déjà disponible / à compléter », parcours de bout en bout |
| 1. Brouillon incomplet | Fiche de poste | Reprise après interruption, contribution en attente (manager) |
| 2. En validation | Validation et équipe | Lecture seule, réponse simulée du valideur |
| 3. À corriger | Validation et équipe | Remarques rattachées aux étapes, renvoi en validation |
| 4. Validée | Récapitulatif | Publication possible, confirmation, écran « publiée », duplication |
| 5. Autre organisation | Démarrage | Circuit court sans DAR (territoriale) : le circuit n'est pas universel |

Scénario fictif : la DREAL Occitanie remplace une chargée de mission rénovation énergétique
(DAR-2026-0318 validée, fiche de poste FP-SECL-2024-012 dans le SIRH, offre similaire publiée en 2025).
Camille Moreau (RH de proximité) crée l'offre ; Julien Lefèvre (manager) contribue et valide ;
Nadia Benali (responsable recrutement) vérifie.

## Architecture du parcours

- **Écran de démarrage** hors étapes : reprendre un brouillon, ou démarrer depuis un besoin (DAR),
  une fiche de poste (SIRH ou document importé), une offre précédente, ou de zéro. Avant de créer,
  on voit ce qui sera repris et ce qui restera à compléter.
- **8 étapes en 4 phases**, navigables librement (colonne de gauche) : Qualifier le besoin (Besoin et
  poste, Fiche de poste) · Rédiger l'offre · Préparer le recrutement (Conditions, Évaluation —
  facultative) · Valider et diffuser (Validation et équipe, Diffusion, Récapitulatif).
- **Panneau de contexte** à droite, permanent : prochaine action et qui la porte, données clés,
  documents liés (DAR, fiche, offre dupliquée), intervenants, historique.
- **Barre de l'offre** en haut : référence, statut, état d'enregistrement, « Enregistrer le brouillon ».

## Choix UX

- **Poste ≠ offre.** Trois natures de blocs, signalées par une bordure et une mention : *usage interne
  — non publié* (gris), *visible par les candidats* (bleu), *paramétrage du recrutement* (violet).
  L'offre se rédige dans un écran à part ; modifier la fiche de poste ne modifie pas l'offre déjà écrite.
- **Origine des données visible champ par champ** : « Repris de la DAR / de la fiche / de l'offre
  dupliquée », puis « · modifié » avec « Rétablir ». La duplication ne recopie pas la DAR ni les dates.
- **Rien n'est remplacé en silence.** Dans l'offre, « Reprendre » remplit une section vide ; si la section
  contient déjà du texte, on demande : remplacer, ajouter à la suite, annuler. Les reformulations sont
  proposées à côté du texte existant et ne s'appliquent que sur action.
- **Peu de champs requis** (marqués *) : ceux qui empêchent de soumettre. Les erreurs ne s'affichent
  qu'après une tentative de soumission, avec une liste cliquable vers chaque champ. Contrôles immédiats
  seulement pour les incohérences (date passée, intitulé trop long, date limite avant début).
- **Avertissements non bloquants** séparés des manques : sigles internes (RIFSEEP, BOP…), sections
  reprises sans retouche, rémunération non évoquée, trop de critères indispensables, question bloquante
  non rattachée à un critère, remarque non traitée.
- **Référentiels souples** : recherche dans le répertoire des métiers avec échappatoire « hors
  répertoire » (saisie libre), métiers associés multiples, plusieurs catégories, plusieurs statuts,
  libellé « Corps » / « Cadre d'emplois » selon le versant.
- **Éligibilité ≠ sélection.** « Qui peut candidater » (profils autorisés) est séparé des critères
  indispensables / souhaités. Catégories et statuts ne sont pas ressaisis : rappel + lien vers l'étape.
- **Évaluation facultative**, sans notation : critères avec importance, points de premier tri, entretiens,
  jury. Un aperçu montre la fiche d'une candidature telle que l'équipe la verra après publication.
- **Circuit de validation dérivé de la situation** : l'étape DAR n'apparaît que si une DAR est requise ;
  validée avant la création, elle est affichée comme déjà obtenue. Les étapes obligatoires viennent du
  paramétrage de l'organisation ; on peut ajouter des relectures facultatives (budget, communication).
- **Publication verrouillée** tant qu'une validation obligatoire manque ; la raison est affichée à côté
  du bouton. En validation ou après validation, l'offre passe en lecture seule ; la modifier la renvoie
  en brouillon (et en validation).
- **Diffusion séparée de la rédaction** : canaux avec ce qu'ils attendent (et lien pour compléter) et les
  actions manuelles restantes, cochables une fois l'offre publiée.
- **Continuité visible** : l'écran « publiée » liste ce qui alimente la suite (éligibilité, questions,
  grille, équipe, indicateurs) et propose la duplication.
- Les commandes qui jouent le rôle d'une autre personne (valideur, contributeur) sont encadrées
  « Simulation » (pointillés violets) : elles n'existeraient pas dans le produit.

## Hypothèses prises (à valider)

- La DAR, quand elle est requise et pas encore obtenue, passe avant les autres validations.
- Après une demande de correction, le circuit reprend à l'étape qui l'a demandée (les validations
  antérieures sont conservées). Renvoyer en validation marque toutes les remarques comme traitées.
- Toute modification d'une offre validée impose une nouvelle validation complète.
- Aucune candidature n'est écartée automatiquement : une question « bloquante » signale seulement au
  premier tri.
- Choisir le Service Public serait alimenté par un connecteur ; les autres canaux restent manuels.
- Les conditions réglementaires générales d'accès ne sont pas modélisées ; la ligne « bénéficiaires de
  l'obligation d'emploi » est indicative.
- Référentiels (métiers, motifs, profils), organismes et personnes : fictifs. L'organisation
  territoriale de la story 5 réutilise les mêmes personnes, par simplicité.

## Questions métier à trancher

1. Qui peut créer une offre : RH de proximité seulement, ou aussi le manager ? Qui peut la publier ?
2. Le circuit de validation est-il paramétré par organisation, par type de recrutement, ou les deux ?
   Qui le configure ?
3. La DAR doit-elle vivre dans l'ATS (avec son propre circuit) ou rester une référence externe ?
4. Quelles informations sont réellement exigées par Choisir le Service Public et les autres canaux ?
5. Après correction, faut-il revalider toutes les étapes ou seulement celle qui a demandé la correction ?
6. Le répertoire des métiers est-il commun aux trois versants ? Que devient un métier « hors répertoire » ?
7. Les critères indispensables et les questions de présélection ont-ils une portée juridique (motif de
   rejet opposable) ? Faut-il un avertissement à la saisie ?
8. Faut-il distinguer « publication » (dans l'ATS) et « diffusion » (sur chaque canal) dans les statuts ?

## Composants

Tout est local au prototype (aucun composant `Csp*` partagé modifié).

- `shared/OffreShell` — cadre (navigation ATS, barre d'offre, étapes, contexte, notifications).
- `shared/StepNav` — étapes groupées par phase, état de complétude, compteurs de manques et de remarques.
- `shared/StepHeader` / `StepFooter` — en-tête d'étape (manques, remarques, lecture seule) et précédent/suivant.
- `shared/ContextPanel` — prochaine action, documents liés, intervenants, historique.
- `shared/FormSection` — bloc typé interne / candidat / recrutement.
- `shared/Field`, `FieldOrigin`, `FieldLabel`, `FieldRow` — origine d'une valeur reprise, « Rétablir ».
- `shared/ListEditor` — liste de libellés éditable (activités, compétences, points de tri).
- `shared/CritereList` — tableau de critères typés (ajout, édition, suppression).
- `shared/OffrePreview` — aperçu candidat.
- `shared/SimulationNote` — encadré des commandes de simulation.
- `data/useOffre` — état partagé (provide/inject), complétude, alertes, circuit, brouillon.
- `data/scenario`, `data/referentiels` — données fictives et états des stories.

## Besoins design system identifiés

- **Champ avec origine de la donnée** (badge « repris de… / modifié / rétablir ») : motif récurrent
  pour toute reprise d'information (SIRH, DAR, duplication). Candidat à un slot `label-end` sur
  `CspInput`, `CspSelect`, `CspTextarea`, `CspCombobox`.
- **`CspTextarea`** : pas de `hint` (alors que `CspInput` en a un) ; le prototype a recréé une zone de
  texte pour l'éditeur d'offre.
- **`CspInput`** : pas de type `date` ; les dates sont saisies au format AAAA-MM-JJ.
- **`CspCallout`** : `role="alert"` systématique — trop fort pour les messages d'information
  (lus d'office par les lecteurs d'écran). Prévoir `role="status"` ou aucun rôle selon la variante.
- **Stepper vertical avec état** (complet / à compléter / facultatif / compteur) : absent du DS.
- **Liste éditable** et **tableau éditable en ligne** (critères) : absents du DS.
- **Carte-radio** (choix du point de départ) : absente du DS.
- **Notification** : `CspToast` demande un provider ; le prototype utilise une région `aria-live` simple.

## Environnement

- `pnpm` est cassé sur ce poste (le binaire installé n'est pas un script Node) et les dépendances
  installées sont en retard sur `main` (`@unhead/vue`, `@testing-library/*` manquants) : un panneau
  d'erreur de type s'affiche par-dessus Storybook (bouton « Close »). Sans lien avec le prototype —
  à signaler à Lucas (`make frontend-install` à refaire).
- Storybook est lancé directement via `node_modules/.bin/storybook`.
