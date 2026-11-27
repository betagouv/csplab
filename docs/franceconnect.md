# Connexion FranceConnect / FranceConnect+ : note d'investigation

Ticket : #2430 (spike). Cette note ne livre aucun code : elle fixe ce que la
documentation de FranceConnect impose, ce que le code actuel permet de réutiliser, et
comment découper l'implémentation (#521).

Sources : documentation partenaires de FranceConnect
(<https://docs.partenaires.franceconnect.gouv.fr/fs/>), six pages lues le 25/11/2026 :
endpoints, scopes, niveaux eIDAS, OIDC FC+, différences FC / FC+. Les pages non lues sont
listées en fin de note ; ce qui en dépend est marqué **à vérifier**.

## Ce qu'on a déjà : ProConnect

Un client OIDC fonctionne pour les agents :

- `infrastructure/authentication/proconnect_client.py` : `authlib` (`OAuth().register`),
  endpoints sous `/api/v2/…`, userinfo renvoyé en JWT signé et vérifié par la JWKS.
- `infrastructure/authentication/proconnect_backend.py` : backend d'authentification qui
  retrouve l'utilisateur par `email__iexact`, synchronise nom et prénom, journalise la
  tentative (`AuditLoginLogModel`, `Canal.PROCONNECT`).
- `presentation/identite/views.py` : vues de connexion, de callback et de déconnexion,
  derrière `PROCONNECT_LOGIN_ENABLED` ; `next` passé par la session et filtré
  (`_safe_next_url`).

Les endpoints de FranceConnect ont la même forme (`/api/v2/authorize`, `/token`,
`/userinfo`, `/jwks`, `/session/end`) : le squelette se réutilise.

## FranceConnect ou FranceConnect+

| | FranceConnect | FranceConnect+ |
|---|---|---|
| Niveau eIDAS (`acr_values`) | `eidas1` seul, obligatoire | `eidas2` ou `eidas3` ; `eidas1` renvoie une erreur |
| Usage visé | démarches non sensibles | démarches sensibles (santé, finance) |
| Fournisseurs d'identité | impots.gouv.fr, Ameli, MSA, La Poste, France Identité | La Poste, France Identité seulement |
| Jetons | signés (ES256 recommandé, RS256 accepté) | signés (ES256 seul) **et chiffrés** (JWE) |
| userinfo | JWS | JWE : le FS publie une clé publique de chiffrement (JWK) |
| Coût | gratuit | gratuit pour la plupart des FS, payant pour certains |

**Recommandation : FranceConnect (eidas1) pour la candidature.** Postuler à un emploi
public n'est pas une démarche sensible au sens de FC+, et FC+ ajoute le chiffrement des
jetons, la clé de chiffrement à exposer, et exclut les comptes impots.gouv / Ameli, que
beaucoup de candidats utilisent. À confirmer avec le métier (marion-dm, #520).

## Ce qui diffère de ProConnect

1. **Identifiant : le `sub`, pas l'email.** Le `sub` est un identifiant technique de 66
   caractères hexadécimaux suivis de `v1`. La doc lue ne dit pas si l'email est vérifié :
   rattacher un compte par email, comme le fait `ProconnectBackend`, ouvre une prise de
   compte (un candidat inscrit avec l'email de quelqu'un d'autre). Il faut stocker le
   `sub` et retrouver le compte par lui. La stabilité du `sub` dans le temps, et le rôle
   du *sector identifier*, sont **à vérifier** (page non lue).
2. **Pas de compte agent.** Un candidat est un `UserModel` avec un `ProfilCandidatModel`
   (`infrastructure/django_apps/users/models.py`). `email` est unique et sert d'identifiant
   Django (`USERNAME_FIELD`) : une création de compte via FC doit gérer un email déjà pris
   (rattachement après preuve de contrôle, ou refus).
3. **Scopes.** `openid` donne le `sub` ; `given_name`, `family_name`, `email` suffisent
   pour un profil minimal. Les données d'identité (naissance, genre) viennent de
   l'habilitation Datapass : n'en demander que le strict nécessaire.
4. **Contrôles obligatoires.** `nonce` et `state` aléatoires, vérifiés au retour
   (`authlib` le fait ; longueur minimale annoncée de 22 caractères sur une page, 32 sur
   une autre, donc prendre 32). Le `acr` de l'ID token est à contrôler : accepter un
   niveau égal ou supérieur à celui demandé.
5. **Déconnexion.** `GET /api/v2/session/end` avec `id_token_hint`, `state` et
   `post_logout_redirect_uri`, par redirection du navigateur : même mécanique que
   `build_proconnect_logout_url`.

## Incohérences de la documentation à lever en bac à sable

- Algorithme de signature de l'ID token : ES256/RS256 d'après la page des niveaux, mais
  l'exemple de la page des endpoints se décode en HS256 (clé = secret client) et la page FC+
  parle de signature « avec le client secret ». À trancher en lisant le `alg` d'un vrai jeton :
  le client `authlib` doit être configuré en conséquence.
- `acr_values` sur FC+ : « requis » sur une page, « optionnel » (eidas3 par défaut) sur une
  autre. Sans objet pour FC.
- Environnement de production de FC : seuls la découverte et la JWKS sont donnés en URL
  complète (`https://oidc.franceconnect.gouv.fr/api/v2/…`) ; la page ne donne pas les autres
  endpoints en production.

## Hors périmètre de cette note

- Démarche d'habilitation (Datapass), bac à sable, mise en production, bouton officiel
  FranceConnect : pages listées ci-dessous, **non lues**. C'est le chemin critique en délai.
- Le cadrage de l'authentification candidat (#520) : parcours, inscription, activation.

## Pistes de découpage pour #521

Dans l'ordre de livraison du dépôt (permission, service, endpoint, schémas, doc), et après
l'habilitation :

1. Modèle de rattachement `(utilisateur, fournisseur, sub)` unique, migration, sans toucher
   à `UserModel`.
2. Service : retrouver ou créer le candidat par `sub`, règle de collision d'email, journal
   d'audit (`Canal.FRANCECONNECT`).
3. Client `authlib` FranceConnect et backend d'authentification, derrière un drapeau
   (comme `PROCONNECT_LOGIN_FLAG`).
4. Vues de connexion, callback, déconnexion ; bouton officiel.
5. Documentation et variables d'environnement.

## Pages de la documentation non lues

Protocole OIDC de base et flux, déconnexion détaillée, `amr`, `sector_identifier`,
chiffrement et signature FC+, erreurs, sessions, bacs à sable FC et FC+, Datapass,
production FC+, bouton officiel.
