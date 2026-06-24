# Web - The CSPLab core server

This service is the first implementation of the future CSP suite developped by
the DGAFP.

## How-to

### Running Django management commands

Django management commands can be run using the `bin/manage` shortcut script
that will execute the well-kown `python manage.py` command in the `web`
service container wrapped with `uv`, _e.g._:

```sh
bin/manage makemigrations
```

is equivalent to:

```sh
docker compose run --rm web uv run python manage.py makemigrations
```

### Seed de données (review apps)

La commande `seed_recruteur_datas` peuple la base de données avec un jeu de
données cohérent pour tester le module recruteur :

| Entité | Quantité |
|---|---|
| Organisme recruteur | 1 (Ministère de la Transition Écologique) |
| Métiers | 2 |
| Agents / recruteurs | 3 |
| Offres actives | 6 |
| Offres archivées | 3 |
| Candidats | 8 |
| Candidatures | 10 |


```sh
bin/manage seed_recruteur_datas
```

La commande est **idempotente** : elle ne recrée pas les données si elles
existent déjà.

Pour réinitialiser et re-seeder :

```sh
bin/manage shell -c "
from infrastructure.django_apps.users.models import UserModel
UserModel.objects.filter(email='marie.dupont@transition-eco.gouv.fr').delete()
"
bin/manage seed_recruteur_datas
```

### Frontend Vue.js (ATS)

Le service web inclut un frontend Vue.js pour l'ATS (Applicant Tracking System).

```bash
make frontend-install   # Installer les dépendances
make frontend-dev       # Lancer Vite dev server (HMR)
make frontend-build     # Build production
```

Documentation : [docs/frontend_vue.md](../../docs/frontend_vue.md)

## License

This work is released under the MIT License (see LICENSE).
