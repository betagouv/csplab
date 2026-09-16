from django.db import migrations


def _normalise(email: str | None) -> str:
    # Volontairement duplique depuis domain.identite.value_objects.email : une
    # migration doit rester figee, elle ne doit pas changer de sens le jour ou
    # la fonction du domaine evolue.
    return (email or "").strip().lower()


def trouver_les_collisions(UserModel) -> dict[str, list]:
    # Comptes dont les emails ne different que par la casse ou les espaces.
    par_forme_normalisee: dict[str, list] = {}
    for pk, email in UserModel.objects.values_list("pk", "email"):
        par_forme_normalisee.setdefault(_normalise(email), []).append(pk)
    return {
        forme: pks for forme, pks in par_forme_normalisee.items() if len(pks) > 1
    }


def normaliser_les_emails(UserModel) -> int:
    collisions = trouver_les_collisions(UserModel)
    if collisions:
        detail = "; ".join(
            f"{forme} -> comptes {pks}" for forme, pks in sorted(collisions.items())
        )
        raise RuntimeError(
            "Migration interrompue : des comptes ne different que par la casse de "
            f"leur email et fusionneraient en un seul. {detail}. "
            "Ces comptes doivent etre arbitres avant de rejouer la migration."
        )

    modifies = 0
    for pk, email in UserModel.objects.values_list("pk", "email"):
        normalise = _normalise(email)
        if normalise != email:
            UserModel.objects.filter(pk=pk).update(email=normalise)
            modifies += 1
    return modifies


def en_avant(apps, schema_editor):
    normaliser_les_emails(apps.get_model("users", "UserModel"))


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_usermodel_username"),
    ]

    operations = [
        # Irreversible : la casse d'origine n'est pas conservee, on ne peut pas
        # la restaurer. Le retour arriere est donc un no-op assume.
        migrations.RunPython(
            en_avant, migrations.RunPython.noop, elidable=True
        ),
    ]
