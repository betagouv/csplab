# Mettre à jour le schéma de l'API

## Pourquoi la CI échoue

Redoc (`api/schema/redoc`) charge `api/schema/public`, qui sert le fichier statique `presentation/static/api/schema.yaml` complété du changelog assemblé, pour éviter l'introspection dynamique de la base. Ce fichier est statique et doit être régénéré à la main à chaque changement des routes de l'API. La CI échoue quand il n'est plus synchronisé avec le code.

## Quand le régénérer

Régénérez le schéma quand vous :
- ajoutez ou retirez une route ;
- modifiez un serializer (champs, types, validateurs) ;
- modifiez les méthodes HTTP ou les permissions d'une vue ;
- ajoutez ou modifiez un décorateur `@extend_schema`.

Le tag `changelog` n'a pas de description dans `schema.yaml` : Redoc charge `/api/schema/public`, qui y ajoute le changelog assemblé à partir de `changelog_api.d/` (voir [changelog_api.md](changelog_api.md)). Le changelog est aussi publié sur `/pages/changelog_api` et en `/api/changelog.md`, `.json` et `.atom`, construits à partir des mêmes fragments : ajouter un fragment ne demande jamais de régénérer le schéma.

Ces routes et `/api/guide.md` sont documentées sous le tag `documentation` (« Changelog et documentation » dans Redoc). Régénérez le schéma quand vous modifiez leur `@extend_schema`, leurs filtres ou `ChangelogSerializer`.

## Découpage du schéma

Les routes sont réparties par des hooks de prétraitement dans `presentation/api/openapi_hooks.py` :

| Route | Fichier de schéma |
|-----|-------------|
| commence par `/api` | `schema.yaml` (public) |
| ne commence pas par `/api` | `internal-schema.yaml` (interne) |
| décorée avec `@extend_schema(exclude=True)` | exclue des deux |


## Comment le régénérer

```bash
mise run web:schema
```

La tâche lance `openapi_schema` plutôt que `spectacular`, pour mettre entre guillemets les chaînes composées uniquement de chiffres, comme `08`, qu'un lecteur YAML 1.2 lirait sinon comme des entiers.

## Validation

L'option `--validate` vérifie que le résultat est un schéma OpenAPI 3 valide avant de l'écrire. Si elle signale des erreurs, corrigez-les avant de committer.
