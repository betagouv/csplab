# ADR-012 : Stratégie de tests du front

**Statut:** Proposé
**Date:** 2026.11.16
**Decideurs:** Lucas P
**Tags:** testing, frontend

---

## Contexte

L'[ADR-001](ADR-001-testing-strategy.md) fixe la stratégie de tests du dépôt, sans dire à quel niveau tester un comportement du front. Une partie de la suite teste chaque composable à part : ces tests cassent quand on déplace une logique, alors que l'écran n'a pas changé. Les tests remplacent aussi les modules d'api par `vi.mock`, si bien que le code qui appelle le serveur et lit sa réponse ne s'exécute jamais.

## Options Considérées

Pour le niveau de test entre le composant et la page :

1. Un test par composant et par composable, comme une partie de la suite le fait : chaque déplacement de logique réécrit des tests sans changement à l'écran.
2. La page comme niveau par défaut : la plupart des tests de composants des features deviendraient non conformes, et une page teste mal un dialogue ou une section qu'elle contient.
3. Le plus petit ensemble que l'utilisateur voit comme un tout, la page quand la route ou les droits comptent : presque tout écran, onglets et panneau de candidature compris, est une destination de route, et les droits viennent des données. Le critère ne sépare donc pas les cas.
4. Monter l'écran selon ce que le test exerce.

Pour la frontière avec le serveur :

1. `vi.mock` sur les modules d'api, comme aujourd'hui : le client HTTP n'est jamais testé.
2. Des tests de contrat entre le front et le back (Pact) : une seule équipe tient le front et le back, et les types générés depuis le schéma OpenAPI signalent déjà un champ renommé, sans outil de contrats à maintenir.
3. Mock Service Worker, qui simule le serveur et laisse tourner le vrai code d'appel.

## Décision

Chaque niveau a son test :

- une fonction pure, par un test unitaire ;
- un composant de `components/base`, par un test de son contrat ;
- un composable, quand sa logique a des branches coûteuses à atteindre par l'écran ;
- ce qui exerce la navigation (changer d'onglet, ouvrir ou fermer le panneau, un paramètre d'URL, une redirection), par le routeur ;
- le composant qu'une route affiche, comme une section d'onglet ou un onglet du panneau, monté directement quand le comportement testé reste dans cet écran ;
- un dialogue, un formulaire de tiroir ou une carte, par l'écran qui les ouvre, sauf s'ils ont un contrat propre ou des branches coûteuses à atteindre.

On garde un test tant qu'il attrape une régression qu'aucun autre test n'attrape. Cette règle précise, pour le front, celle de l'ADR-001 qui teste un comportement une seule fois.

Les tests simulent le serveur avec Mock Service Worker. Les réponses par défaut d'une feature sont dans `src/test/handlers/<feature>.ts`, typées par le schéma de l'API. On migre feature par feature, en commençant par les recrutements.

Les conventions d'écriture des tests restent dans [`frontend_conventions.md`](../frontend_conventions.md).

## Conséquences

- Un refactoring à l'intérieur d'un écran laisse ses tests verts.
- Les tests exécutent le client HTTP, et un champ renommé par le back fait échouer la vérification des types des réponses simulées.
- Tant que la migration n'est pas finie, les deux façons de simuler le serveur coexistent.
- Les composants qu'une route affiche sont aujourd'hui rangés tantôt dans `views/`, tantôt dans `components/` : il faut les ranger au même endroit et nommer de la même façon les sections d'onglet, d'une feature à l'autre.
