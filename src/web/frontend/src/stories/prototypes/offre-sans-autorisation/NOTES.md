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

## Manques design system (repris du proto ATS)

- CspTextarea, CspCheckboxGroup, CspRadioGroup : pas d'aide (« hint ») ni de message d'information ; contourné
  par `ChampSimple.vue`.
- CspInput : pas de type date.
