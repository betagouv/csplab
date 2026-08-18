from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task, lock_task

from infrastructure.di.identite.identite_factory import create_identite_container
from infrastructure.exceptions.exceptions import TaskError


@db_periodic_task(crontab(hour="6", minute="0"))
@lock_task("import-etablissements-finess-periodic")
def import_etablissements_finess_periodic():
    import_etablissements_finess()


@db_task()
def import_etablissements_finess():
    container = create_identite_container()
    logger = container.logger_service()
    usecase = container.import_etablissements_finess_usecase()

    try:
        result = usecase.execute()
        logger.info(
            "✅ Import FINESS terminé : %d créés, %d mis à jour",
            result["created"],
            result["updated"],
        )
        if result["errors"]:
            logger.warning("⚠️ %d erreurs rencontrées", len(result["errors"]))
            for error in result["errors"]:
                logger.warning(
                    "Etablissement %s: %s", error["entity_id"], error["error"]
                )
    except Exception as e:
        raise TaskError(
            message="Failed to import etablissements FINESS",
            details={"error": str(e)},
        ) from e
