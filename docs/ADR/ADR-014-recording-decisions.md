---
status: proposé
date: 2026-11-27
decision-makers: Équipe
supersedes: DDR-000
---

# ADR-014 : Enregistrer une décision

## Contexte et problème

Comment une personne qui arrive, ou un agent de code, lit-il le statut d'une décision, et comment vérifie-t-il qu'elle est appliquée ? L'équipe enregistre ses décisions dans deux séries, les ADR et les décisions de design, et les agents de code de chaque membre lisent ces fichiers à chaque tâche. Quand l'équipe ne retrouve pas une décision, elle la rediscute, et un agent écrit du code qui la contredit.

Le relevé de l'existant est dans l'[epic de la documentation](https://github.com/betagouv/csplab/issues/2529).

## Décision

On écrit les ADR et les décisions de design avec le même en-tête, les mêmes sections et le même cycle de vie. On range chaque décision selon l'[ADR-015](ADR-015-documents-by-nature.md).

### En-tête

L'en-tête est un bloc YAML en tête du fichier. Ses clés `status`, `date`, `decision-makers`, `consulted` et `informed` sont celles de MADR, en anglais comme les identifiants du dépôt ([ADR-011](ADR-011-identifier-language.md)), et on y ajoute les clés des liens entre décisions.

- `status` : proposé, accepté, rejeté, déprécié ou remplacé ;
- `date` : date de la dernière modification de la décision, au format AAAA-MM-JJ ;
- `decision-makers` : les personnes qui décident ;
- `consulted` et `informed` : les personnes consultées et les personnes informées, quand il y en a ;
- `supersedes` et `superseded-by`, `amends` et `amended-by` : les identifiants des décisions liées. On écrit chaque lien dans les deux décisions, dans la même PR.

### Sections

- Contexte et problème : on pose le problème en une question, puis on écrit les contraintes durables, techniques ou métier, dont l'équipe tient compte pour y répondre, en trois phrases au plus. Une contrainte durable reste vraie une fois la décision appliquée. On écrit le relevé de l'existant (fichiers, écarts, comptages) dans l'issue que la décision cite : il cesse d'être vrai quand la décision est appliquée.
- Décision : on écrit la règle que l'équipe applique.
- Options considérées : on liste les options réellement envisagées pendant la rédaction ou la revue de la décision, avec la raison pour laquelle on a écarté chacune, pour que personne ne les repropose sans élément nouveau. On omet la section quand on a envisagé une seule option.
- Conséquences : on écrit ce que la décision change dans le système une fois appliquée, les caractéristiques qu'elle améliore et celles qu'elle dégrade, puis ce qu'elle impose à l'équipe.
- Confirmation : on nomme ce qui vérifie que la décision est appliquée, une règle de lint, un test ou le relecteur d'une PR, et le mode du contrôle (en erreur, en avertissement, à la main). Avec ce contrôle, l'équipe voit qu'une décision au statut « accepté » a cessé d'être appliquée.
- Questions ouvertes : on écrit ce que l'équipe doit encore trancher. On omet la section quand tout est tranché.

### Cycle de vie

- On propose une décision dans une PR, seule ou avec le code qui l'applique.
- Tant qu'une question reste ouverte, on laisse la décision au statut « proposé », y compris après la fusion.
- Quand l'application demande plusieurs PR, on écrit le plan de migration dans des issues, et la décision les cite.
- On garde le fichier et le numéro d'une décision remplacée. Quand la décision qui la remplace est acceptée, on passe son statut à « remplacé » et on réduit le fichier à son en-tête et à une phrase qui renvoie à cette décision, et on retrouve son texte dans l'historique git.

## Options considérées

1. Un format par série : on garde l'en-tête des ADR et celui des décisions de design. On écrit alors de deux façons le lien entre une ADR et une décision de design, et la CI lit deux formats.
2. Un en-tête, des sections et un cycle de vie communs aux deux séries, d'après [MADR 4.0](https://adr.github.io/madr/). C'est l'option retenue.
3. Pour le cycle de vie, garder en entier le texte d'une décision remplacée, comme le conseillent [Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) et [Martin Fowler](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html) : on relit ses raisons sur place, et un agent de code qui cherche dans le dossier lit un texte périmé.

## Conséquences

- Une personne qui arrive ou un agent de code lit dans l'en-tête d'une décision son statut, les personnes qui l'ont prise et les décisions qui la remplacent ou l'amendent.
- Le dossier des ADR et celui des décisions de design contiennent le texte des décisions en vigueur et l'en-tête des décisions remplacées.
- Cette ADR remplace la décision de design [« Pourquoi des DDR »](../../src/web/frontend/src/stories/ddr/content/ddr-000-pourquoi-des-ddr.md) : on écrit les décisions de design dans le format décrit ici.
- On lit moins vite les raisons passées : le relevé qui a motivé une décision est dans une issue sur GitHub, et le texte d'une décision remplacée dans l'historique git.
- L'auteur d'une décision écrit un en-tête complet, et le lien dans la décision liée.
- On réécrit les ADR et les décisions de design existantes dans ce format, selon les issues de l'[epic de la documentation](https://github.com/betagouv/csplab/issues/2529).

## Confirmation

La CI vérifie par `mise run check` l'en-tête de chaque décision et la présence de chaque lien dans les deux décisions, en erreur. Ce test est décrit dans [son issue](https://github.com/betagouv/csplab/issues/2531). Le relecteur d'une PR vérifie les sections à la main.

## Questions ouvertes

- Qui accepte une décision, et à quel moment : les personnes nommées dans `decision-makers`, par leur approbation de la PR, ou l'équipe en rétrospective ?
