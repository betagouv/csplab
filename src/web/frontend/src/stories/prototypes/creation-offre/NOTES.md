# Notes — Prototype création d'offre

## Itération 3 — enseignements complémentaires (20 octobre 2026)

Même parcours en 4 étapes, sans nouvelle étape ni nouvel écran de création. Ajouts : une **liste des offres**
(point d'entrée, consultation), la **sauvegarde automatique**, la **séparation fiche / DAR / offre**,
le **multi-postes**, un **historique** lisible et des **notifications** réglables.

Scénario : Camille prépare une offre pour **3 postes de gestionnaire de paie**. La fiche de poste
FP-SG-2026-007 (import SIRH fictif) donne l'intitulé, le service, la localisation, la catégorie, les
missions et 3 activités ; il manque les compétences, le profil et l'environnement. Interrompue hier, elle
reprend son brouillon depuis la liste, demande un complément à Isabelle Fournier (cheffe du bureau RH),
rédige l'offre, puis soumet : la DAR part en validation avec l'offre.

Stories (`Version simplifiée`) : 0. Liste · 1. Brouillon paie · 2. Soumise · 3. Corrections ·
4. Validée (démo isolée) · 5. Sans validation (démo isolée). Les stories 0 à 3 partagent les mêmes
dossiers : ce qui est fait dans l'une se retrouve dans les autres, même après rechargement de la page
(sessionStorage). Lien « Réinitialiser les données de démonstration » en bas de la liste.

### Changements

| Enseignement | Traitement | Où |
| --- | --- | --- |
| A. Fiche de poste base du travail, qualité variable | Reprise de la fiche ; ce qui manque est dit une fois dans le résumé de la section (« à compléter : compétences, profil… »), section ouverte d'office, champs vides avec une indication ; « Demander à [manager] de compléter » (réponse simulée) | Étape 1 |
| B. DAR ≠ offre | La fiche de poste devient « Fiche de poste — contenu de la DAR ». À la soumission, ce contenu est **figé** (consultable dans Suivi) ; l'offre se rédige à part et peut être comparée au texte source (« Comparer avec la DAR »), jamais l'inverse. Si la fiche change après validation, une phrase le signale, la DAR ne bouge pas | Étapes 1 et 2, Suivi |
| C. Brouillon | Sauvegarde automatique 1,5 s après la dernière saisie, indicateur discret (« Modifications en cours… / Enregistrement en cours… / Enregistré à 15:50 »), bouton « Enregistrer le brouillon », « Quitter » qui enregistre et revient à la liste, reprise à l'étape où l'on s'était arrêté. Aucune perte au rechargement | Barre de l'offre, liste |
| D. Historique | Regroupé par jour, une icône par type (création, reprise, modifications, contribution, soumission, validation, correction, publication) ; les enregistrements successifs d'une même session tiennent sur une ligne | Suivi |
| E. Tableaux personnalisables | Liste des offres avec choix des colonnes (dont **code poste**, DAR, étape, date limite…), conservé pendant la session ; filtres simples | Liste |
| F. Plusieurs postes par offre | « Nombre de postes à pourvoir » dans l'essentiel du poste, codes poste facultatifs (« 2 sur 3 renseignés ») ; repris dans le récapitulatif, l'aperçu candidat (« 3 postes à pourvoir ») et la liste | Étape 1 |
| G. Doubles saisies | Localisation, service, catégorie repris de la fiche ; badges de provenance affichés **seulement si la valeur a été modifiée** (pour proposer « Rétablir ») | Étape 1 |
| H. Notifications | Fréquence des courriels de nouvelles candidatures (chaque / toutes les 5 / récapitulatif quotidien / aucun), dans Suivi et sur l'écran « publiée » ; aucun envoi | Suivi, écran publiée |

Statuts distingués : **Brouillon** (modifiable, enregistré automatiquement) · **Soumise à validation**
(lecture seule, DAR figée) · **Validée** · **Publiée**. Un brouillon peut être enregistré même incomplet.

### Hypothèses à confirmer

- La DAR reprend la fiche de poste et est **figée à la soumission** ; elle est validée telle que soumise.
  Une modification après validation demanderait une nouvelle version de DAR (non prototypé).
- La DAR est préparée **dans le même dossier** que l'offre et part en validation avec elle, en première
  étape du circuit. Alternative à tester : DAR validée d'abord, offre rédigée ensuite.
- Le contenu exact de la DAR (champs) et son format de publication légale ne sont pas modélisés.
- Une offre couvre N postes **identiques** ; des postes différents (lieux, quotités) feraient l'objet
  d'offres distinctes. Le niveau de détail par poste (code, date de prise de poste…) reste à déterminer.
- Les codes poste viennent du SIRH ; leur saisie manuelle est un pis-aller.
- Les notifications sont réglées par personne et par offre (pas pour toute l'équipe).
- La sauvegarde automatique enregistre aussi les brouillons incomplets ; aucune règle de complétude ne
  bloque l'enregistrement.

## Itération 2 — version simplifiée (20 octobre 2026)

Retour d'Alice sur l'itération 1 : trop complexe, trop d'étapes, trop de rouge. Hypothèse explorée :
**un parcours commun à tous, avec des informations conditionnelles et des options facultatives
qui n'apparaissent que si elles sont utiles.** La complexité organisationnelle est portée par le produit
(paramétrage), pas par l'utilisateur.

Stories : `Prototypes/Création d'offre/Version simplifiée` (l'itération 1 reste dans `…/Itération 1 (archive)`).

| Story | Ce qu'elle montre |
| --- | --- |
| 0. Nouvelle offre | Organisation avec DAR et validation ; préremplissage depuis une DAR / fiche / offre |
| 1. Brouillon repris | Reprise, contribution du manager en attente |
| 2. En validation | Lecture seule, bandeau unique, réponse simulée dans « Suivi » |
| 3. Corrections demandées | Remarques affichées dans la section concernée, renvoi en validation |
| 4. Validée | Publication directe depuis « Vérifier et finaliser », duplication |
| 5. Sans circuit de validation | Même parcours ; l'action finale devient « Publier l'offre » |

### Analyse de l'itération 1

**1. Étapes regroupées (9 écrans → 4 étapes)**
- Écran de démarrage → intégré en haut de l'étape 1 (bandeau « partez de l'existant » + fenêtre de choix),
  réduit à une ligne une fois la source appliquée.
- Besoin et poste + Fiche de poste → **Définir le poste** (fiche de poste repliée).
- Offre pour les candidats → **Rédiger l'offre** (inchangée sur le fond, allégée).
- Conditions + Évaluation → **Conditions de candidature** (évaluation repliée).
- Validation et équipe + Diffusion + Récapitulatif → **Vérifier et finaliser** ; le circuit, les remarques,
  l'équipe et l'historique passent dans le volet **Suivi** (bouton de la barre d'offre), accessible à tout moment.

**2. Informations affichées selon le contexte**
- Type de contrat : seulement si le poste est ouvert aux contractuels.
- DAR : seulement si l'organisation utilise des DAR (paramétrage). Reprise d'une DAR validée → une simple
  ligne de rappel, sans champ. Sinon un champ facultatif « si votre recrutement en nécessite une ».
  La question « une DAR est-elle nécessaire ? » est supprimée (règle métier non documentée).
- Poste remplacé : seulement si le motif est une vacance ou un remplacement.
- Corps / cadre d'emplois : libellé selon le versant.
- Étape DAR du circuit : seulement si une référence DAR non validée est saisie.

**3. Fonctionnalités devenues facultatives (repliées, avec un résumé)**
- Fiche de poste (missions, activités, compétences, conditions particulières) — n'est plus requise.
- Informations complémentaires : métier du répertoire, motif, date de prise de poste, quotité, nombre de postes, corps.
- Questions de présélection ; évaluation et entretiens (grille, premier tri, jury).
- Sections de l'offre « Présentation de l'organisme », « Conditions », « Informations pratiques ».
- Ajout d'étapes facultatives au circuit : retiré (le circuit vient du paramétrage).
- Métiers associés : retirés de cette version.

**4. Alertes supprimées ou déplacées**
- Bandeau « N informations requises » en tête de chaque étape : supprimé.
- Compteurs orange et pastilles de remarques dans la navigation : remplacés par une coche discrète
  (étape vue et complète).
- Astérisques rouges : supprimés ; seuls les champs facultatifs du socle sont signalés « (facultatif) »
  (convention DSFR).
- Callouts permanents (hypothèses réglementaires, « lecture seule », « DAR passera en premier »,
  « pas de blocage ») : supprimés ; un seul bandeau d'état quand l'offre est en validation, à corriger ou validée.
- Bloc « Relecture éditoriale » de l'étape offre : déplacé en « suggestions » repliées dans le récapitulatif.
- Erreurs de champ : uniquement après une tentative de soumission/publication, ou pour une donnée
  réellement invalide (intitulé trop long, format de date, date limite avant le début).
- Les remarques des valideurs restent visibles, dans la section concernée, sur fond bleu (pas rouge).

**5. Interactions redondantes retirées**
- Ressaisie des profils autorisés : proposés à partir des statuts ouverts de l'étape 1.
- Catégorie et statuts ne sont plus rappelés comme champs à l'étape 3 (une ligne + « Modifier »).
- Reprise section par section dans l'offre : un seul bouton « Préremplir » pour toutes les sections vides
  (plus de dialogue « remplacer / ajouter » puisqu'on ne remplit que le vide).
- Fenêtre de confirmation de publication : supprimée — le récapitulatif fait office de vérification.
- Vue « côte à côte » : retirée (Rédaction / Aperçu suffisent ; aperçu aussi depuis le récapitulatif).
- Panneau de contexte permanent à droite : retiré (doublait la barre d'offre et le récapitulatif).
- Écran « Validation et équipe » : remplacé par une phrase dans le récapitulatif
  (« Validation prévue : Julien Lefèvre, puis Nadia Benali ») et le volet Suivi.

### Classement des particularités métier

| Socle commun (visible) | Conditionnel (selon le contexte) | Facultatif (replié) |
| --- | --- | --- |
| Intitulé, organisme, service, localisation | Contrat (si contractuels) | Fiche de poste détaillée |
| Catégorie(s), statuts ouverts | DAR (si l'organisation en utilise) | Métier du répertoire, motif, dates, quotité, corps |
| Présentation du poste, missions, profil, modalités de candidature | Circuit de validation (selon paramétrage) | Questions de présélection |
| Profils acceptés (proposés), critères de sélection | Poste remplacé (si vacance / remplacement) | Grille d'évaluation, premier tri, entretiens |
| Canaux et date limite (avant publication) | Informations attendues par un canal choisi | Reformulation, contribution du manager |

### Trois niveaux de messages (récapitulatif)

- **À compléter pour soumettre / publier** (bloquant) : liste avec « Compléter » qui ouvre le bon champ.
  Liseré bleu ; rouge seulement après une tentative.
- **À compléter avant publication** (non bloquant pour la soumission) : canaux, date limite, remarques
  non traitées. Fusionné avec la liste bloquante quand l'organisation n'a pas de validation.
- **Suggestions** (repliées) : sigles internes, rémunération non évoquée, sections reprises sans retouche…

### Action finale selon le contexte

- Validation restante → « Soumettre à validation » (ou « Renvoyer en validation »), avec la phrase qui dit
  qui validera.
- Pas de circuit, ou validation obtenue → « Publier l'offre ».
- En validation → « Retirer de la validation ».

### Nouveaux composants (itération 2)

`shared/Disclosure` (section repliable avec résumé), `shared/Panel`, `shared/QuestionsEditor`,
`shared/EvaluationEditor`, `data/redaction` (préremplissage de l'offre), et dans `variants/simplifie/` :
`ShellSimple`, `EtapesNav`, `SuiviDrawer`, `SourcePanel`, `RemarquesSection`, `EtapeFooter`, `useEtapes`
et les 4 étapes. Le store commun accepte désormais des règles désactivables (`exclure`) et un paramétrage
d'organisation « sans validation ».

### Questions ouvertes ajoutées

- Le circuit de validation peut-il dépendre du type de recrutement (ex. contractuel vs titulaire) ?
  Qui le paramètre ?
- Les profils acceptés sont-ils vraiment distincts des statuts ouverts, ou un seul champ suffit-il ?
- La fiche de poste doit-elle rester facultative si l'organisation l'exige pour la DAR ?
- Publier sans confirmation est-il acceptable, ou faut-il pouvoir dépublier rapidement ?

---

## Itération 1

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
