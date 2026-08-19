from contextlib import nullcontext
from datetime import date
from unittest.mock import MagicMock, Mock
from uuid import uuid4

from ddd.unit_of_work import IUnitOfWork
from referentiel.value_objects.verse import Verse

from application.identite.usecases.import_etablissements_finess import (
    BATCH_SIZE,
    ImportEtablissementsFinessUsecase,
)
from domain.commons.constants import SYSTEM_UTILISATEUR_ID
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.organisme import Organisme
from domain.identite.errors.organisme_errors import EtablissementInvalideError
from domain.identite.gateways.organisme_gateway_interface import (
    OrganismeImportResource,
)
from domain.identite.value_objects.siret import SIRET
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.mappers.organisme_finess_mapper import REFERENTIEL_FINESS

RESOURCE = OrganismeImportResource(
    url="https://static.data.gouv.fr/finess.json.gz",
    millesime=date(2026, 8, 18),
)


def _make_organisme(nom="Clinique du Docteur Convert", external_id="010780195"):
    return Organisme.build(
        entity_id=uuid4(),
        nom=nom,
        versant=Verse.FPH,
        localisation=None,
        siret=SIRET("77220148900022"),
        parent_id=None,
        external_id=external_id,
        referentiel=REFERENTIEL_FINESS,
        millesime="2026-08-18",
        gestion_ats=False,
    )


def _upsert_result(organismes, created_organismes=None, updated_organismes=None):
    created_organismes = (
        organismes if created_organismes is None else created_organismes
    )
    updated_organismes = updated_organismes or []
    return {
        "created": len(created_organismes),
        "updated": len(updated_organismes),
        "errors": [],
        "created_organismes": created_organismes,
        "updated_organismes": updated_organismes,
    }


def _make_usecase(organismes, upsert_batch_result=None):
    organisme_gateway = MagicMock()
    organisme_gateway.find_latest_resource.return_value = RESOURCE
    organisme_gateway.stream_organismes.return_value = iter(organismes)

    organisme_repository = MagicMock()
    organisme_repository.upsert_batch.return_value = (
        upsert_batch_result or _upsert_result(organismes)
    )

    unit_of_work = Mock(spec=IUnitOfWork)
    unit_of_work.atomic.return_value = nullcontext()

    audit_log_writer = MagicMock(spec=AuditLogWriter)

    usecase = ImportEtablissementsFinessUsecase(
        organisme_gateway=organisme_gateway,
        organisme_repository=organisme_repository,
        logger=LoggerService(),
        unit_of_work=unit_of_work,
        audit_log_writer=audit_log_writer,
    )
    return usecase, organisme_gateway, organisme_repository, audit_log_writer


def test_import_upserts_organismes_from_finess_stream():
    organisme = _make_organisme()
    usecase, organisme_gateway, organisme_repository, _ = _make_usecase([organisme])

    result = usecase.execute()

    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == []
    organisme_gateway.stream_organismes.assert_called_once_with(RESOURCE)
    (batch,), _ = organisme_repository.upsert_batch.call_args
    assert batch == [organisme]


def test_import_logs_domain_events_for_created_and_updated_organismes():
    created = _make_organisme(external_id="010780195")
    updated = _make_organisme(nom="Autre nom", external_id="010787190")
    usecase, _, _, audit_log_writer = _make_usecase(
        [created, updated],
        upsert_batch_result=_upsert_result(
            [created, updated],
            created_organismes=[created],
            updated_organismes=[updated],
        ),
    )

    usecase.execute()

    drain_events_calls = audit_log_writer.drain_events.call_args_list
    expected_call_count = 2
    assert len(drain_events_calls) == expected_call_count
    for call in drain_events_calls:
        assert call.kwargs["utilisateur_id"] == SYSTEM_UTILISATEUR_ID
    aggregates = [call.kwargs["aggregate"] for call in drain_events_calls]
    assert aggregates == [created, updated]

    created_events = created.collect_events()
    assert len(created_events) == 1
    assert created_events[0].event_name == "OrganismeCree"

    updated_events = updated.collect_events()
    assert len(updated_events) == 1
    assert updated_events[0].event_name == "OrganismeModifie"


def test_import_reports_invalid_etablissement_as_error():
    error = EtablissementInvalideError("010780195", ValueError("SIRET invalide"))

    def _raising_stream(resource):
        raise error
        yield  # pragma: no cover - unreachable, makes this a generator function

    organisme_gateway = MagicMock()
    organisme_gateway.find_latest_resource.return_value = RESOURCE
    organisme_gateway.stream_organismes.side_effect = _raising_stream

    organisme_repository = MagicMock()
    unit_of_work = Mock(spec=IUnitOfWork)
    unit_of_work.atomic.return_value = nullcontext()

    usecase = ImportEtablissementsFinessUsecase(
        organisme_gateway=organisme_gateway,
        organisme_repository=organisme_repository,
        logger=LoggerService(),
        unit_of_work=unit_of_work,
        audit_log_writer=MagicMock(spec=AuditLogWriter),
    )

    result = usecase.execute()

    assert result["created"] == 0
    assert len(result["errors"]) == 1
    assert result["errors"][0]["entity_id"] == "010780195"
    organisme_repository.upsert_batch.assert_not_called()


def test_import_flushes_in_batches():
    organismes = [
        _make_organisme(nom=f"Etablissement {i}", external_id=f"01078{i:04d}")
        for i in range(BATCH_SIZE + 1)
    ]
    usecase, _, organisme_repository, _ = _make_usecase(organismes)
    organisme_repository.upsert_batch.side_effect = lambda batch: _upsert_result(batch)

    result = usecase.execute()

    expected_batch_count = 2
    assert organisme_repository.upsert_batch.call_count == expected_batch_count
    first_call_batch, second_call_batch = (
        call.args[0] for call in organisme_repository.upsert_batch.call_args_list
    )
    assert len(first_call_batch) == BATCH_SIZE
    assert len(second_call_batch) == 1
    assert result["created"] == len(organismes)
