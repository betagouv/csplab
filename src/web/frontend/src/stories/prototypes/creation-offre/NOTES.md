# Notes — Prototype création d'offre

## Itération 8 — parcours cible et DAR paramétrée par l'organisme (22 octobre 2026)

Alignement sur le schéma « Parcours de création d'un recrutement » fourni par Alice, et sur les captures de
l'outil actuel (Choisir le Service Public : création et détail d'une DAR, publication d'une offre).

**Parcours** : Référentiel des fiches → **Lancer un recrutement** (3 sources : fiche de poste, offre existante,
saisie manuelle — le mode « fichier » est retiré de la création ; les fiches « issues d'un document » restent
dans le référentiel) → **Offre rédigée** (contenu candidat + aperçu) → **DAR** si l'organisme l'exige →
**Préparer l'offre pour la publication** (nombre de postes, modalités de recrutement, date limite, contact) →
**Publication** (supports).

**La DAR n'est plus un choix à la création** : c'est un paramètre de l'organisme (nouvelle page
« Paramètres de l'organisme », simulée). Le parcours s'adapte : avec DAR, l'offre a un onglet « DAR » et le
bouton de fin de rédaction mène à la saisie de la DAR ; sans DAR, « Terminer la rédaction » mène directement
à la préparation. Le changement de paramètre s'applique aux offres en rédaction dont la DAR n'est pas soumise.

**Onglet DAR** (inspiré des sections CSP, en plus sobre) : entité, type de DAR, employeur, descriptif employeur
et service, intitulé, catégorie, **nombre de postes**, description, motif (pour éviter les appels des valideurs),
pièces jointes. Préremplie depuis la fiche. **Vrai état « Brouillon »** (fini « BROUILLON » dans l'intitulé),
enregistrement automatique, soumission (contenu figé), décision simulée Valider / Refuser avec motif ;
historique propre à la DAR. Refus → la DAR redevient modifiable, l'offre revient en rédaction.

**Préparer et publier** : nombre de postes repris de la DAR (écart signalé), modalités proposées depuis la
fiche, date limite ; tableau des supports groupés comme dans CSP (sites web avec CSP en support maître,
jobboards, multi-diffuseurs) avec état, début, fin ; après publication, Publier / Arrêter par support ;
« Arrêter les publications et archiver ».

### Décisions d'Alice (22 octobre 2026)
- **Superviseur** : le besoin de DAR est paramétré par le superviseur de l'organisme, commun à tout l'organisme
  (dans un premier temps). La page « Paramètres de l'organisme » est en lecture seule pour le responsable du
  recrutement ; une simulation permet d'agir en superviseur.
- **Nombre de postes** : une DAR peut valider en une fois le besoin pour plusieurs postes identiques ; l'offre
  reprend ce nombre, qui devient non modifiable.
- **Après validation** : certains champs de l'offre sont verrouillés pour garantir la validité de la DAR
  (prototype : nombre de postes et lieu, rappelés « validé par la DAR »). Le texte éditorial reste modifiable
  pendant la relecture, et la publication reste une action manuelle du responsable du recrutement.
- **Champs de la DAR** : liste et caractère obligatoire non connus ; le formulaire est présenté comme indicatif.

### Hypothèses restantes
- Liste exacte des champs verrouillés après validation (nombre de postes et lieu dans le prototype).
- La DAR est saisie après la rédaction de l'offre (ordre du schéma) ; le contenu est en lecture seule pendant
  la validation.

### Points à confirmer
1. Champs du formulaire de DAR et champs obligatoires, selon le type de DAR.
2. Liste des champs de l'offre verrouillés par une DAR validée.
3. Que faire si un champ verrouillé doit changer (nouvelle DAR, demande de modification) ?

## Itération 7 — ATS : fiches de poste et offres d'emploi (21 octobre 2026)

Nouvelle variante, code autonome : `variants/ats/` ; stories `Prototypes/Création d'offre/ATS — fiches de
poste et offres`. Les itérations 1 à 6 sont rangées sous `Archives/`.

**Deux objets distincts et reliés** : la **fiche de poste** (référentiel durable ; origine ATS, SIRH simulé
ou document ajouté) et l'**offre d'emploi** (opération de recrutement + annonce). Toute offre est rattachée
à une fiche ; une fiche peut avoir plusieurs offres, ou aucune.

**Écrans** : 1 Tableau de bord (compteurs par état, offres à faire avancer) · 2 Fiches de poste (recherche,
filtre par origine, actives/archivées, colonnes) · 3 Détail d'une fiche (contenu, origine, synchronisation
simulée, offres rattachées, historique, modification avec enregistrement automatique, « Lancer un
recrutement ») · 4 Créer une offre (4 modes, rattachement toujours affiché) · Espace d'une offre en 3 onglets :
5 Rédaction, 6 Validation et publication, 7 Suivi · Offres d'emploi (filtre par état, colonnes).

**Cycle de vie** : En cours de rédaction → En cours de validation (DAR) → À publier → Publiée → Archivée.
La DAR est conditionnelle : le recruteur indique si elle est nécessaire ; sans DAR, la rédaction passe
directement à « À publier ». Publier est une action distincte (canaux + date limite).

**Rédaction** : formulaire de l'annonce (titre, présentation, nombre de postes, missions, profil,
compétences indispensables / souhaitables, modalités, lieu, rémunération, télétravail, conditions, date
limite, contact). À droite, au choix : **aperçu candidat** (mis à jour en direct) ou **fiche de poste source**
(consultation seule). Chaque champ a un conseil court (et un exemple à la demande), au plus une alerte
discrète (manque essentiel, sigles, phrase trop longue, trop de compétences indispensables, rémunération
absente), et « Repris de la fiche » / « Reprendre le texte de la fiche ». « Mettre en forme » transforme
une liste brute en puces sans changer les mots. Enregistrement automatique + « Enregistrer le brouillon ».

**Quatre modes de création** : depuis une fiche (préremplie) · depuis un fichier (lecture simulée ; nouvelle
fiche « issue d'un document » ou rattachement à une fiche existante) · saisie manuelle (l'essentiel saisi
crée la fiche de référence) · depuis une ancienne offre publiée ou archivée (contenu copié, nouvelle offre
indépendante, fiche de rattachement vérifiable). Chaque carte dit à quelle fiche l'offre sera rattachée.

**Données** : fiches « Gestionnaire de paie » (ATS), « Chargé·e de recrutement » (SIRH), « Chef·fe de projet
numérique » (document), « Assistant·e administratif·ve », « Responsable informatique » (SIRH, sans offre),
« Chargé·e d'accueil » (archivée). Offres : paie en rédaction (3 postes), recrutement en validation DAR,
chef de projet à publier (sans DAR), assistant publiée (base de duplication), accueil archivée.

### Hypothèses
- Le besoin de DAR est déclaré par le recruteur pour chaque offre (règles réelles inconnues).
- Le contenu de l'offre est en lecture seule pendant la validation de la DAR ; « À publier » peut revenir en
  rédaction sans nouvelle DAR (la DAR porte sur le besoin, pas sur le texte de l'annonce).
- Une demande de correction sur la DAR renvoie l'offre en rédaction avec la remarque.
- Modifier une fiche SIRH dans l'ATS est possible, mais pourrait être écrasé par la synchronisation (règle à définir).
- Un document ajouté crée par défaut une nouvelle fiche ; l'extraction du contenu est simulée.

### Points à confirmer
1. Qui décide du besoin de DAR et sur quels critères ?
2. Règles de synchronisation SIRH ↔ ATS (champs maîtres, conflits, fiches modifiées localement).
3. Une offre publiée peut-elle être modifiée ? Avec quelle traçabilité ?
4. Que devient une offre si sa fiche est archivée ou fortement modifiée ?
5. Le texte de l'offre doit-il être revalidé si la DAR porte aussi sur le contenu de l'annonce ?

## Itération 6 — référentiel des fiches de poste (21 octobre 2026)

Nouvelle hypothèse produit : **la fiche de poste est le point d'entrée**. Les RH maintiennent un
référentiel de fiches durables ; depuis une fiche, ils **lancent un recrutement** avec DAR ou par
**création directe de l'offre**. Les deux parcours convergent vers la même création d'offre ; la
publication reste une action distincte.

**Modèle** (dans `data/`) : `FichePoste` (référentiel, `fiches.ts`) → recrutement (`OffreState`,
`dossiers.ts`, référence REC-…, lié par `ficheId` et `ficheVersion`) → DAR éventuelle (contenu figé à la
soumission) → offre (OFF-…, même numéro). Au lancement, la fiche est **copiée** dans le recrutement :
modifier la fiche ensuite n'écrase ni la DAR ni l'offre (vérifié dans le prototype).

**Navigation** : Fiches de poste (point d'entrée) · Recrutements (suivi) · Mes offres.

| Écran | Contenu |
| --- | --- |
| Fiches de poste | Recherche (intitulé, code poste, mot-clé), filtre service, actives / archivées, colonnes configurables (code poste, métier, recrutements, « à compléter »…), « Nouvelle fiche de poste » |
| Fiche de poste | Consultation (poste, missions, compétences, environnement) ; « À compléter : … » en une ligne ; Modifier (sauvegarde automatique) ; Archiver / Réactiver ; recrutements associés (avancement, version reprise) ; historique ; « Lancer un recrutement » |
| Lancer un recrutement | Fenêtre unique : nombre de postes + parcours (avec DAR / création directe), règle de choix affichée comme hypothèse |
| DAR | Reprise de la fiche (modifications propres à la DAR), brouillon enregistré automatiquement, « Soumettre la DAR » ; une fois soumise : lecture seule, validations en cours (réponse simulée), puis « Poursuivre vers la création de l'offre » |
| Création d'offre (commune) | Configurer le recrutement (rappel de ce qui est repris de la fiche et de la DAR, postes, codes, date limite, contact, canaux, conditions ; options repliées) → Rédiger l'offre (titre, textes, mise en forme, reformulation, comparaison avec la DAR, aperçu) → Vérifier et finaliser (créer l'offre, puis interrupteur de publication) |
| Recrutements / Mes offres | Suivi avec avancement fiche → DAR / création directe → offre → publication ; colonnes configurables |

Fil du processus en tête d'un recrutement : **Fiche de poste** (cliquable : ouvre la fiche) · **DAR** ou
« Création directe » · **Offre** · **Publication**.

Scénario testé : fiche « Gestionnaire de paie » → recrutement 3 postes avec DAR → soumission refusée tant
que le type de contrat manque → brouillon enregistré → soumission → validation simulée → configuration →
rédaction (préremplissage) → création de l'offre, publication désactivée. Second cas : fiche
« Responsable informatique » → création directe → arrivée dans la même création d'offre.

### Choix UX

- Le référentiel est l'écran d'accueil ; la fiche se lit sans être ouverte en édition.
- Lancer un recrutement tient dans une seule fenêtre (pas d'assistant) ; on arrive directement sur la
  DAR ou sur la configuration de l'offre selon le parcours.
- La DAR a sa propre vue ; l'offre ne la modifie jamais. Les informations reprises sont rappelées en tête
  de la configuration plutôt que redemandées.
- Création et publication restent deux actions ; la publication est désactivée par défaut.
- Les recrutements d'une fiche indiquent la version de la fiche reprise.

### Hypothèses

- Le choix « avec DAR / création directe » est laissé au RH au lancement (règle réelle inconnue).
- Un recrutement copie la fiche ; il n'y a pas de synchronisation automatique ensuite.
- Une offre ne peut être créée qu'une fois la DAR validée (quand il y en a une) ; elle peut être préparée
  pendant la validation.
- Une fiche archivée ne permet plus de lancer de recrutement, mais reste consultable avec ses recrutements.
- Les fiches sont créées dans l'ATS ; l'origine SIRH est seulement anticipée (mention « Origine »).

### Points à confirmer

1. Règles qui imposent une DAR (organisation, statut, catégorie, type de poste, montant ?).
2. Une modification de la fiche doit-elle être proposée aux recrutements en cours (et à la DAR non soumise) ?
3. Qui maintient le référentiel (RH de proximité, recrutement, manager) et avec quels droits ?
4. Source de référence de chaque donnée quand un SIRH fournira des fiches.
5. Niveau de détail par poste quand un recrutement en couvre plusieurs (codes, dates, lieux).
6. Faut-il un statut « clôturé » pour un recrutement terminé (poste pourvu) ?

## Itération 5 — besoins et offres (21 octobre 2026)

Retour d'Alice : le mot « recrutements » ne convient pas. Processus à rendre visible :
**déclaration du besoin (= rédaction de la fiche de poste) → validation par DAR ou non → rédaction de
l'offre → publication.** Deux pages : **Mes besoins en recrutement** et **Mes offres**.

- **Menu latéral** : « Mes besoins en recrutement » · « Mes offres » (déplié, libellés visibles).
- **Mes besoins en recrutement** : une ligne par besoin ; colonne « Avancement » (4 pastilles
  besoin · validation · offre · publication + l'étape en clair), colonne « Validation » (référence DAR ou
  « Sans DAR ») ; filtres « En cours de déclaration ou de validation », « Prêts pour l'offre », « Avec une
  offre » ; bouton « Déclarer un besoin ». Colonnes personnalisables (dont code poste).
- **Mes offres** : les offres démarrées ; état « En rédaction / Créée, non publiée / Publiée », date
  limite… ; bouton « Rédiger une offre » qui renvoie aux besoins prêts. Colonnes personnalisables.
- **Fil du processus** en tête de chaque dossier : Besoin · Validation · Offre · Publication, avec l'état
  de chacun (« DAR soumise », « Sans DAR », « À rédiger », « Non publiée »…). « Besoin » et « Offre » sont
  cliquables ; les sous-étapes de l'offre (Rédiger · Compléter · Vérifier et publier) n'apparaissent
  qu'en vue offre. Remplace les badges de statut.
- **Vue « Besoin »** : « Déclarer le besoin » = fiche de poste (au premier plan, plus repliée), puis
  « Validation du besoin » : *Avec une DAR* ou *Sans DAR*. Action de fin selon le cas : « Soumettre la DAR
  à validation », « Préparer l'offre en attendant » (DAR soumise), « Rédiger l'offre » (DAR validée ou
  sans DAR). Si la DAR est soumise ou validée, la vue est une fiche de consultation en lecture seule.
- Ouvrir une ligne de « Mes besoins » ouvre la vue besoin ; une ligne de « Mes offres » ouvre l'offre là
  où on s'était arrêté. Le fil d'Ariane et « Quitter » ramènent à la page d'origine.
- Nouveau cas de démonstration : besoin **sans DAR** (chargé·e de communication interne, CDD 1 an) avec
  offre en rédaction.

Hypothèses : le choix DAR / sans DAR est fait par le recruteur pour chaque besoin (à confirmer : règle de
l'organisation, du type de recrutement ou du statut ?) ; une offre peut être préparée pendant la
validation de la DAR mais créée seulement après ; sans DAR, l'offre peut être rédigée dès que les
informations essentielles du besoin sont renseignées.

## Itération 4 — la DAR validée comme source de l'offre (20 octobre 2026)

Organisation observée (CSP uniquement) : fiche de poste → DAR → validation de la DAR → offre créée à partir
de la DAR → quelques champs propres à l'offre → publication activée ou non. Le prototype suit ce fil sans en
faire un modèle universel (story 5 : une autre organisation fait aussi valider l'offre).

**Trois objets distincts** : la fiche de poste (source) → la DAR (contenu figé à la soumission, validé tel
quel) → l'offre (reprend la DAR, contenu éditorial retravaillable). **Cinq états non confondus**, affichés
séparément dans la barre et la liste : DAR en brouillon · DAR soumise · DAR validée · offre créée
(publication désactivée) · publication activée.

Scénario principal (story 1, ou ligne DAR-2026-0331 de la liste) : DAR validée le 15 octobre par
Hélène Robert pour 3 postes de gestionnaire de paie. Ouvrir la DAR démarre l'offre, préremplie. Le texte
repris est brut (BRH/SG, EVS, IJ, « ; ») : « Mettre en forme » le passe en puces sans changer un mot,
« Proposer une reformulation » propose un texte candidat, « Comparer avec la DAR » montre la version
validée, inchangée. On quitte, on reprend (rien n'est perdu, même après rechargement), on crée l'offre :
la publication reste désactivée jusqu'à ce qu'on l'active (date limite requise).

### Changements

- **Liste « Recrutements »** : une ligne par DAR, colonnes « État DAR » et « État offre » (« À créer »,
  « En rédaction », « Créée, non publiée », « Publiée ») ; filtre « Offres à créer ». Colonnes toujours
  personnalisables (code poste, réf. offre…).
- **Étape 1 « Préparer le besoin »** : si la DAR est soumise ou validée, simple fiche de consultation en
  lecture seule (intitulé, service, localisation, catégorie, postes, texte de la DAR repliable). Rien à
  ressaisir. Si la DAR est en brouillon, formulaire de l'itération 3 + « Soumettre la DAR à validation ».
- **Étape 2 « Rédiger l'offre »** : titre de l'annonce (éditorial) distinct de l'intitulé de la DAR ;
  sections préremplies avec le texte brut de la DAR (« Texte repris de la DAR — à adapter ») ;
  « Mettre en forme », reformulations propres au scénario paie, comparaison en ligne avec la DAR ;
  aperçu candidat. Aucun écran de comparaison dédié.
- **Étape 3 « Compléter l'offre »** : nombre de postes (prérempli depuis la DAR, rappel « DAR : 3 »),
  codes poste, date limite, prise de poste, contact candidats, publication sur Choisir le Service Public
  (autres canaux derrière un lien) ; qui peut candidater ; critères, questions et évaluation repliés.
- **Étape 4 « Vérifier et créer »** : action selon l'état — « Soumettre la DAR » (DAR en brouillon),
  attente (DAR soumise), « Soumettre l'offre » (organisation qui valide l'offre), sinon « Créer l'offre ».
  Après création : interrupteur « Publication » désactivé par défaut ; activation refusée avec la liste de
  ce qui manque (date limite, canal) ; notifications ; duplication.
- **Suivi** : validation de la DAR simulée (« Réponse d'Hélène »), contenu de la DAR figé, historique
  incluant les événements de la DAR (création, soumission, validation) et de l'offre.

### Hypothèses retenues pour le prototype

- L'offre peut être **préparée** pendant que la DAR est en validation, mais **créée** seulement après
  validation de la DAR.
- Les informations communes (intitulé, service, localisation, catégorie, statuts) viennent de la DAR et
  ne se modifient pas depuis l'offre ; seuls le titre de l'annonce et les textes sont éditoriaux.
  Le **nombre de postes** et les **codes poste** sont modifiables dans l'offre (rappel de la valeur DAR).
- La date limite et un canal sont nécessaires pour **activer la publication**, pas pour **créer** l'offre.
- Les modalités de candidature viennent d'un modèle de l'organisme (absent de la DAR).
- Une offre créée reste modifiable tant que la publication n'est pas activée.

### Questions métier à trancher

1. Règles de modification des champs administratifs communs après validation de la DAR (intitulé,
   localisation, nombre de postes…) : nouvelle version de DAR, simple correction, ou libre dans l'offre ?
2. Si la DAR est modifiée après création de l'offre, faut-il répercuter, signaler, ou ignorer ?
3. Conditions supplémentaires qui empêcheraient de publier (au-delà de la date limite) ?
4. Détail à gérer par poste quand une offre en couvre plusieurs (codes, dates, lieux différents ?).
5. Une offre publiée peut-elle être modifiée ? Avec quelle traçabilité vis-à-vis de la DAR ?

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
