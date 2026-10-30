from django.db import migrations

# competences_requises was a list of texts before #2152 and is now a Markdown
# text: an empty list becomes null, other lists are joined with line breaks.
COMPETENCES_REQUISES_EN_TEXTE = r"""
UPDATE offers
SET criteria = jsonb_set(
    criteria,
    '{competences_requises}',
    COALESCE(
        (
            SELECT to_jsonb(string_agg(competence, E'\n' ORDER BY position))
            FROM jsonb_array_elements_text(criteria -> 'competences_requises')
                WITH ORDINALITY AS competences(competence, position)
        ),
        'null'::jsonb
    )
)
WHERE jsonb_typeof(criteria -> 'competences_requises') = 'array'
"""


class Migration(migrations.Migration):
    dependencies = [
        ("referentiel", "0058_offer_zone_depuis_departement"),
    ]

    operations = [
        migrations.RunSQL(
            sql=COMPETENCES_REQUISES_EN_TEXTE,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
    ]
