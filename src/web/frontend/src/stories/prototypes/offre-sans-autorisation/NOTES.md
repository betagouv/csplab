# Proto « Offres sans autorisation (MVP) »

D'après le doc PO « Création manuelle des offres » (17/11/2026). On prototype d'abord le parcours **sans autorisation**,
pour avoir un parcours carré avant le circuit d'autorisation. Le proto « ATS — fiches de poste et offres » (avec
validation) reste à côté, inchangé, dans `creation-offre/`.

Ce dossier repart d'une copie des écrans du proto ATS, épurée de tout ce qui touche à la validation.

## Parcours

- **Mes offres d'emploi** : tableau (brouillons, publiées, dépubliées) filtré par puces de statut. Colonnes : intitulé
  (service · lieu · référence), statut + « depuis N jours », prochaine étape (jamais vide), responsable, mise en
  ligne, dépublication (rouge à moins de 7 jours), candidatures (lien vers le recrutement), menu « … ».
- **Créer une offre** : formulaire vide ou duplication (MVP ; la fiche de poste est post-MVP). Le créateur devient
  Responsable. La duplication remet le nombre de postes à 1 et vide les dates et les champs d'autorisation.
- **Formulaire en 5 étapes** : Annonce, Informations internes, Formulaire de candidature, Processus (facultatif),
  Équipe (facultatif). Rien n'est exigé pour enregistrer un brouillon ; « Passer cette étape » sur les étapes
  facultatives.
- **Page de l'offre** : sections modifiables (y compris une fois publiée) à gauche, encart de l'état à droite.
- **Publier** (parcours séparé, choix d'Alice) : aperçu candidat à gauche ; à droite, ce qui manque, la date de fin
  (date limite de candidature, au moins un mois sauf urgence), l'emplacement « Multidiffusion » (bientôt), le bouton.
  Publication immédiate.
- **Publiée** → **Dépubliée** : à la date de fin (retrait automatique) ou par « Retirer l'offre ». Les candidatures
  restent à traiter. **Prolonger** une offre dépubliée la remet en ligne.
- **Droits** : « Créer » et « Publier » par agent (Paramètres). Sans « Publier », l'agent prépare l'offre mais ne peut
  ni publier, ni prolonger, ni retirer (story 9).

## Choix et écarts avec le doc

- Le doc place « Publication » en 6e étape du formulaire ; Alice a choisi un **parcours Publier séparé**.
- Après création, on modifie l'offre sur la **page à sections** (choix d'Alice), pas en rejouant les étapes.
- **Compétences** : celles du métier cochées, ajout libre possible (doc). Changer de métier remplace les compétences
  cochées : c'est la question 1 « à trancher » du doc.
- Informations internes sans autorisation : seulement les références internes (les 6 champs d'autorisation
  n'apparaissent que si l'organisme a un circuit).
- Dates saisies au format AAAA-MM-JJ : CspInput n'accepte pas `type="date"` (manque du design system, à voir avec Lucas).

## Alignement sur le tableau des champs (PO, 17/11/2026)

- Annonce réorganisée selon les catégories du tableau : métadonnées, Le poste, Cadre du recrutement, Profil
  recherché, Conditions de travail, Employeur, Localisation. Mentions « Champ obligatoire » selon la colonne Modalité.
- Ajouts : lien vers l'avis de vacance au JO, diplôme d'État requis, spécialisation, langues avec niveau
  (niveau obligatoire si une langue est ajoutée), « Pas de lieu fixe », géolocalisation (adresse, pré-remplie avec
  celle de l'organisme), lieu d'affectation. Télétravail et Management deviennent des listes oui / non.
- Devenus facultatifs : descriptif du profil recherché. Devenus obligatoires : versant, nombre de postes (max 10),
  nature de l'emploi, descriptif de l'employeur, adresse.
- Publication : date de fin seule (= date limite de candidature, ≥ aujourd'hui + 1 mois
  sauf urgence). Pas de programmation (retour Alice, 18/11/2026) : l'offre est mise en ligne le jour où on publie, seule la date de fin se choisit.
- Champs « DAR » (motif, agent remplacé, code poste, RIFSEEP, cycle) : masqués sans circuit d'autorisation.
- « Mettre l'offre en pause » : remplacée par « Retirer l'offre » dans le menu « … » de la liste (retour PO, point 6 :
  pas de distinction entre pause et dépublication ; on remet en ligne en prolongeant).

## Retours PO du 19/11/2026

Numérotation L/F reprise d'une version reformulée par IA. Le document original de la PO (reçu ensuite) a été relu :
deux écarts corrigés, décrits sous F2 et sous « pause » ci-dessus. Le reste est conforme.

Liste des offres
- L1 Onglets par phase : En préparation, En ligne (ouvert par défaut), Terminées, Toutes. Avec un circuit
  d'autorisation, les statuts de validation se rangeront dans « En préparation ».
- L2 Colonne Statut seulement dans « Toutes » ; plus de « depuis N jours », la date de mise en ligne suffit.
- L3 Filtres dans un tiroir : responsable, service, lieu, catégorie.
- L4 En ligne : tri par date de fin croissante. Terminées : les plus récentes d'abord.
- L5 « dans N jours » écrit sous la date de fin (plus seulement la couleur), icône d'alerte à moins de 7 jours.
- L6 « Suivre les candidatures » retiré de Prochaine étape (« — » quand il n'y a rien à faire).
- L7 Plusieurs responsables : « Camille Moreau +1 », liste complète au survol.
- L8 « Créer une offre » en bouton principal. L9 « Dupliquer » ouvre directement le formulaire pré-rempli.
- L10 « Retirer l'offre » remplace « Mettre en pause » (voir plus haut).
- L11 « Compléter l'annonce » affiche « 10 / 13 champs obligatoires ».
- L12 « Fin de publication » partout. L13 « Statut » partout. L14 Recherche : « Intitulé, lieu, référence ».
- L15 Sous-titre : « en préparation, en ligne et terminées ».

Formulaire
- F1 Une suite de huit écrans de gauche à droite, la même à la création et sur la page de l'offre : Le poste, Cadre
  du recrutement, Profil et conditions, Employeur et lieux, Informations internes, Candidature, Étapes de
  recrutement (facultatif), Équipe de recrutement (facultatif). Étapes cliquables, cochées quand complètes.
- F2 (point 4 du document original) Processus et Équipe restent dans la suite d'écrans, mais reprennent les écrans
  existants : `EtapesRecrutementOffre.vue` copie `EtapesRecrutementList` (textes, liste ordonnable, encadré) et
  `EquipeRecrutementOffre.vue` copie `EquipeRecrutementSection` (tableau Membre, Rôle, Poste, Courriel). À
  l'intégration : brancher les vrais composants. Journal d'activité : sorti du formulaire, ouvert depuis le menu
  « … » de l'offre, présenté comme l'historique d'une candidature (« N activités récentes »).
- F3 Messages d'information en bandeau au-dessus du titre (`PageAts`, prop `bandeaux`).
- F4 Récapitulatif « Avant de publier » : coché / à remplir par étape, « Plus que N champs obligatoires… ».
- F5 Astérisque rouge sur les champs obligatoires (au lieu de « Champ obligatoire »).
- F6 Les alertes « à corriger » n'apparaissent qu'après une tentative de publication (`tentatives` dans aide.ts).
- F7 Versant et organisme de rattachement retirés du formulaire (déduits de l'organisme).
- F8 Catégorie, Corps, puis Grade. Nature de l'emploi : un choix unique (fonctionnaires uniquement, fonctionnaires
  et contractuels, contractuels uniquement).
- F9 Plusieurs lieux (« Ajouter un lieu »), chacun avec une adresse à suggestions (simulées ; la Base adresse
  nationale en vrai) et sa géolocalisation. « Pas de lieu fixe » gardé en attendant la DGAFP.
- F10 Publication programmée retirée (18/11). F11 « Multidiffusion : bientôt » retiré. F12 Mention « pas de
  circuit d'autorisation » retirée.

Réponses aux questions
- Q1 Sous l'intitulé : service · lieu(x) · référence. Le service vient de la fiche de poste du jeu de données (ou
  de l'offre dupliquée) : il n'est saisi nulle part dans le formulaire. Le lieu vient de l'étape « Employeur et
  lieux ». La référence est la référence interne de l'ATS (OFF-…). À trancher : ajouter un champ « Service ».
- Q2 « Champs obligatoires seulement » : pas fait. Avec les étapes et le récapitulatif, on va directement aux
  champs manquants ; à tester avant d'ajouter ce filtre.

## Restructuration demandée par Alice (25/11/2026)

- **Étapes** : 7 étapes en deux parties. *Annonce visible du candidat* : Le poste, Le cadre du recrutement, Le métier (page dédiée au métier et aux compétences), Le profil recherché (ex-« Profil et conditions »), L'environnement de travail (ex-« Employeur et lieux ») — ordre et titres revus le 25/11. *Paramétrage des candidatures* : Formulaire (questions), Documents (pièces demandées).
- **Retirées** : Informations internes (France Travail, référence interne), Étapes de recrutement, Équipe de recrutement. Les composants `FormInterne`, `EtapesRecrutementOffre`, `EquipeRecrutementOffre` et `RecapPublication` restent dans le dossier, inutilisés.
- **Création** : plus d'écran de choix. « Créer une offre » ouvre le formulaire vide ; « Dupliquer » (menu « … ») ouvre le formulaire pré-rempli. Une page par étape, étapes groupées par partie à gauche. Enregistrement automatique, « Enregistrer et quitter » à tout moment ; « Publier » s'active quand tous les champs obligatoires sont remplis.
- **Publication** : page « Vérifier et publier » (aperçu candidat + date de fin) → « Valider la publication » → fenêtre de succès : « Afficher le recrutement » ou « Retourner aux offres ».
- **Page de l'offre** : structure inspirée de Malt. En-tête, « Accéder à : », bloc « À compléter avant de publier » (champs obligatoires manquants par étape, bouton « Compléter »), puis un bloc par étape avec un crayon. La modification se fait dans le bloc (Annuler / Enregistrer). Prolonger : fenêtre ; Retirer : menu « … ».
- **Choix pris par Claude, à valider** :
  - modification sur place dans le bloc (pas de panneau latéral) ;
  - blocs Formulaire et Documents verrouillés une fois l'offre publiée ;
  - « Publier » désactivé tant qu'il manque des champs obligatoires.
- **Écran du recrutement** : simplifié pour le proto (0 candidature juste après la publication). Dans l'outil, c'est l'écran existant du recrutement qui s'ouvre.
- **À tester** : place du métier et des compétences (étape dédiée ou dans « Le profil recherché »).

## Blocage technique (à signaler à Lucas)

- 19/11/2026 : les dépendances installées sur le poste sont celles d'une branche plus récente (proto/vision-csp).
  Storybook affiche des erreurs de types sans lien avec le proto (fenêtre « vue-tsc », à fermer). La réinstallation
  (`pnpm install --frozen-lockfile`) échoue : pnpm 12.9.1 plante au démarrage (« SyntaxError: Invalid or unexpected
  token » sur son propre exécutable). Le prototype s'affiche et fonctionne malgré tout.

## Manques design system (repris du proto ATS)

- CspTextarea, CspCheckboxGroup, CspRadioGroup : pas d'aide (« hint ») ni de message d'information ; contourné
  par `ChampSimple.vue`.
- CspInput : pas de type date.

## Tableau « Mes offres d'emploi » par statut (Alice, 25/11/2026)

- Onglets par statut : Brouillon, En ligne, En pause, Archivée, Toutes (remplacent En préparation / En ligne / Terminées).
  Pas d'onglet « À valider » : ce proto reste sans autorisation (choix d'Alice). À reprendre dans le proto avec autorisation.
- Colonnes, socle commun : Offre d'emploi (intitulé, service · lieu · référence), Statut, Responsable, Activité sur l'offre,
  Fin de publication (En ligne, En pause selon le cas, Toutes), Candidatures (sauf Brouillon), Actions.
  Retirées : « Prochaine étape » et « Mise en ligne ».
- Activité sur l'offre : « Modifiée le… », « Publiée le… », « Mise en pause le… », « Archivée le… ».
- Interprétation à valider : « En pause » = l'ancien statut « Dépubliée » (retirée, prolongeable). La fin de publication
  ne s'affiche pour une offre en pause que si la date n'est pas passée (une échéance existe encore).
- Les offres archivées sont maintenant visibles dans la liste. Deux offres fictives ajoutées : une en pause avant sa date de fin,
  une archivée.
- Statut « Brouillon » renommé « En préparation » partout (onglet, badges, page de l'offre, formulaire) — demande d'Alice.

## Offres en pause : « Remettre en ligne » (Alice, 25/11/2026)

- Une offre en pause n'est pas forcément à prolonger : des recruteurs la mettent en pause quand ils ont assez de candidatures
  à traiter, puis la remettent en ligne s'ils en veulent d'autres. Le CTA devient « Remettre en ligne » (page de l'offre,
  menu « … » de la liste, colonne d'action).
- La fenêtre de remise en ligne garde la date de fin si elle n'est pas passée (modifiable) ; sinon elle en demande une nouvelle.
- Proposition à valider : l'action « Retirer l'offre » s'appelle désormais « Mettre en pause », comme le statut obtenu.

## « Mes offres d'emploi » : actions à faire (Alice, 25/11/2026)

- Encart « À faire » entre l'en-tête et les onglets, par priorité : offres qui se terminent dans moins de 7 jours (orange),
  puis offres prêtes à publier (vert). Les offres en préparation à compléter n'y sont pas : pas d'urgence (Alice).
  Un clic applique un filtre existant et ouvre l'onglet concerné : « Statut : En préparation · Prête à publier » ou
  « Fin de publication : Dans moins de 7 jours » (nouveaux filtres du tiroir). Pas d'état coloré sur la carte choisie.
  La vue filtrée est annoncée au-dessus du tableau (« Vue filtrée : » + étiquettes supprimables + « Supprimer les filtres »).
  Les compteurs des onglets restent les totaux, même filtrés (Alice).
  Une carte sans offre disparaît, l'encart aussi. Pas de filet sous l'en-tête dans ce cas.
- Bouton d'action sur la ligne, avant le menu « … » : Continuer, Publier, Prolonger (ouvre directement la fenêtre).
- Sans autorisation, « publier une offre validée » devient « publier une offre prête » (tous les champs obligatoires remplis).
- Colonne Statut : badge dans « Toutes » ; texte simple dans « En préparation » (Brouillon / Prête à publier ; plus tard
  À valider, Validée…) ; absente des autres onglets.
- Besoin design system : slot entre l'en-tête de page et les onglets (fait ici dans PageAts, propre au proto).
- Une seule offre concernée par une carte « À faire » : titre de la carte (« Une offre arrive à échéance », « Une offre prête
  à publier »), titre de l'offre (lien vers sa page), puis bouton d'action. Ancienne version : échéance
  (« Se termine dans 4 jours » / « Prête à publier ») et porte le bouton d'action (Prolonger, Publier). Pas d'ouverture
  automatique de l'offre : le comportement de la carte resterait imprévisible. À partir de 2 offres, la carte filtre le tableau.
- Cartes « À faire » harmonisées (Alice) : titre (« Une offre arrive à échéance » / « 2 offres prêtes à publier »), titre de
  l'offre s'il n'y en a qu'une, puis bouton : l'action (Prolonger, Publier) pour une offre, « Voir les offres » (filtre) sinon.
- Puis retour à la flèche (Alice) : un utilisateur rouvre l'offre avant de publier ou prolonger. Toute la carte est cliquable ;
  une offre → sa page ; plusieurs → le tableau filtré. Plus de bouton dans les cartes.

## Retours PO sur la liste et le formulaire (26/11/2026)

1. Carte « À faire » orange : « Une offre sera dépubliée automatiquement dans 4 jours » (plusieurs : « N offres seront
   dépubliées automatiquement dans moins de 7 jours »). Interprétation à valider : la PO a cité « Une offre va être dépubliée
   automatiquement… ». Le statut obtenu reste « En pause ».
2. Onglet « En préparation » : colonne « Champs obligatoires remplis » (x / y + jauge, verte quand c'est complet).
3. Action d'un brouillon incomplet : « Compléter » (au lieu de « Continuer »).
4. Dates saisies au format JJ-MM-AAAA (date de vacance, fin de publication, prolongation) ; stockées en AAAA-MM-JJ.
5. Corps et grades : plusieurs choix dans une liste fixe ; les corps proposés suivent la catégorie, les grades suivent les
   corps choisis. Liste illustrative (5 corps), à remplacer par le référentiel officiel.
6. Étape « Le métier » : Famille puis Métier (RMFP+) ; le sous-texte « Le domaine et le sous-domaine en sont déduits » est retiré.
   Familles fictives (reprises des domaines de l'extrait RMFP+ du proto).
7. « Ajouter une compétence » : seulement depuis la liste des compétences du RMFP (extrait fictif). Les compétences déjà
   saisies dans les données de démo restent affichées.
8. Langues : choix dans une liste fixe (10 langues, proposition).
9. Formulaire de candidature : bloc « Questions oui / non » avec RQTH et Fonctionnaire. Posées par défaut ; un interrupteur
   par question permet de ne pas la poser (Alice). Rappelées dans le bloc Formulaire de la page de l'offre. Libellés proposés, à valider.
- Écran étroit (Alice) : dans le formulaire en étapes, les parties 1 et 2 s'affichent côte à côte au-dessus du formulaire
  (plus de liste collée en haut qui recouvrait les champs).
- Besoin design system : sélection multiple dans une liste (combobox + étiquettes), faite ici dans ChoixMultiple (propre au proto) ;
  champ date au format JJ-MM-AAAA (ChampDate, propre au proto).

## Carte « fin de publication » raccourcie (27/11/2026)

- Titre : « 1 offre arrive en fin de publication » / « N offres arrivent en fin de publication », avec un repère orange
  « J-4 » (plusieurs offres : l'échéance la plus proche). Remplace « … sera dépubliée automatiquement dans N jours ».
- À valider avec la PO : son retour 1 demandait de dire clairement que la dépublication est automatique.
- Lecteur d'écran : « J-4 » est lu « fin dans 4 jours ».

## Revue UI avec l'équipe (27/11/2026)

**Page de l'offre**
- Onglets à la place de « Accéder à » : Annonce, Paramètres du recrutement, Diffusion, Activité. Les trois premiers
  reprennent les parties de la création. Le bloc « À compléter » et l'alerte de fin restent au-dessus des onglets.
- Onglet Activité : historique de toutes les modifications, avec la date et la personne (« Automatique » pour le
  retrait à la date de fin). Enregistrer un bloc ajoute une ligne avec les champs changés (ex. « « Le poste » modifié :
  Intitulé de l'offre »). Remplace le tiroir « Journal d'activité ». Modifications passées : fictives.
- Onglet Diffusion d'une offre en ligne : état de la publication sur chaque site. Un site ajouté après la publication
  est publié tout de suite (proposition).
- À trancher : l'onglet s'appelle « Paramètres du recrutement », la partie 2 de la création « Paramétrage des candidatures ».

**Création**
- Partie 3 « Diffusion » (étape 8) : d'abord « Diffuser et gérer les candidatures dans l'ATS » ou « Diffuser
  uniquement », puis multidiffusion ou non, avec les sites à cocher (liste indicative, fictive).
  Propositions : « Diffuser uniquement » demande un lien ou une adresse électronique pour postuler (obligatoire),
  et la partie 2 affiche qu'elle ne s'applique pas. La gestion des candidatures ne change plus après publication ;
  les sites, si. Pas de recrutement créé pour une offre gérée hors ATS.
- Retiré de la liste des sites : « Place de l'emploi public » (ancien nom de Choisir le Service Public).
- Compétences RMFP+ : « Savoir-faire » ou « Connaissance » en texte secondaire à côté de chaque compétence, et dans la
  recherche. Classement fictif. Le RMFP+ compte environ 2 000 savoir-faire et plus de 1 000 connaissances (chiffres de l'équipe).
- Questions oui / non (RQTH, fonctionnaire) : « Non posée / Posée », présenté comme les documents, à la place du switch.
- Conditions de travail déplacées dans l'étape 5 « L'environnement de travail » (avec le temps de travail obligatoire).
- Lieux : un premier lieu est affiché d'emblée ; « Ajouter un autre lieu » sert à en mettre plusieurs.

**Liste des offres : offres téléversées (proposition à discuter)**
- Deux offres téléversées fictives, en ligne : étiquette « Téléversée » sous l'intitulé, « Hors ATS » dans la colonne
  Candidatures, pas de recrutement (absentes de « Mes recrutements »). Même affichage pour une offre « Diffuser uniquement ».
- Filtre « Candidatures » : gérées dans l'ATS, gérées hors ATS, offres téléversées.
- Question ouverte : d'où viennent les offres téléversées (import d'un fichier, flux) et qui les téléverse ?
