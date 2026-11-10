import logging
from datetime import datetime, timezone
from itertools import chain
from typing import Optional
from uuid import UUID

import sentry_sdk
from pydantic import ValidationError
from referentiel.entities.organisme import Organisme

from domain.entities.raw_organisme import RawOrganisme
from domain.gateways.organismes_cleaner import IOrganismesCleaner
from domain.gateways.siret_lookup_gateway import ISiretLookupGateway
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from domain.value_objects.siret_candidate import SiretCandidate
from infrastructure.exceptions.exceptions import DilaSiretNotFound
from infrastructure.gateways.siret_matching import (
    ScoredCandidate,
    best_associative_candidate,
    best_candidate,
    best_public_candidate,
    embassy_matches,
    is_potential_employer,
    name_score,
)

logger = logging.getLogger(__name__)

BATCH_SIZE = 500
DEFAULT_DILA_SIRET_MIN_SCORE = 0.85

_SIRET_LENGTH = 14
_SIREN_LENGTH = 9
_EMBASSY_TYPE = "Ambassade ou mission diplomatique"
# Sentry groups every alert into a single issue listing the affected services.
_DILA_SIRET_NOT_FOUND_FINGERPRINT = ["dila-siret-not-found"]


def _is_siret(query: str) -> bool:
    return query.isdigit() and len(query) == _SIRET_LENGTH


def _with_parent(organisme: Organisme, parent_id: Optional[UUID]) -> Organisme:
    return Organisme.build(
        entity_id=organisme.entity_id,
        nom=organisme.nom,
        versant=organisme.versant,
        localisation=organisme.localisation,
        siret=organisme.siret,
        parent_id=parent_id,
        external_id=organisme.external_id,
        referentiel=organisme.referentiel,
        millesime=organisme.millesime,
        date_creation=organisme.date_creation,
        date_derniere_activite=organisme.date_derniere_activite,
        gestion_ats=organisme.gestion_ats,
    )


class CleanRawOrganismesUsecase:
    def __init__(
        self,
        organismes_cleaner: IOrganismesCleaner,
        raw_organisme_repository: IRawOrganismeRepository,
        siret_lookup_gateway: Optional[ISiretLookupGateway] = None,
        dila_siret_min_score: float = DEFAULT_DILA_SIRET_MIN_SCORE,
    ) -> None:
        self._organismes_cleaner = organismes_cleaner
        self._raw_organisme_repository = raw_organisme_repository
        self._siret_lookup_gateway = siret_lookup_gateway
        self._dila_siret_min_score = dila_siret_min_score

    async def execute(self, referentiel: str) -> list[Organisme]:
        total_raw = 0
        total_cleaned = 0
        deduped_organismes: list[Organisme] = []
        # entity_id -> entity_ids of the ancestors, closest first (DILA only).
        ancestors: dict[UUID, list[UUID]] = {}
        depths: Optional[dict[UUID, int]] = (
            {} if referentiel == OrganismeReferentiel.DILA else None
        )

        while True:
            raw_batch = await self._raw_organisme_repository.find_uncleaned(
                referentiel, BATCH_SIZE
            )
            if not raw_batch:
                break

            await self._resolve_missing_dila_sirets(raw_batch)

            cleaned_ids = []
            cleaned_batch: list[Organisme] = []
            for raw_organisme in raw_batch:
                cleaned_ids.append(raw_organisme.id)
                try:
                    organisme = self._organismes_cleaner.clean(raw_organisme)
                except ValidationError as e:
                    logger.warning(
                        "Invalid data for raw organisme %s: %s",
                        raw_organisme.external_id,
                        e,
                    )
                    continue
                except Exception:
                    logger.exception(
                        "Unexpected error cleaning raw organisme %s",
                        raw_organisme.external_id,
                    )
                    continue
                if organisme is not None:
                    cleaned_batch.append(organisme)
                    ancestor_ids = self._organismes_cleaner.dila_ancestor_ids(
                        raw_organisme
                    )
                    if ancestor_ids:
                        ancestors[organisme.entity_id] = ancestor_ids
                    if depths is not None:
                        depths[organisme.entity_id] = len(ancestor_ids)

            await self._raw_organisme_repository.mark_as_cleaned_batch(
                cleaned_ids, datetime.now(tz=timezone.utc)
            )
            total_raw += len(raw_batch)
            total_cleaned += len(cleaned_batch)

            # Dedupe per batch: bounds memory by unique SIRETs, not raw count.
            deduped_organismes = self._organismes_cleaner.dedupe_by_siret(
                chain(deduped_organismes, cleaned_batch), depths
            )

            if len(raw_batch) < BATCH_SIZE:
                break

        if ancestors:
            deduped_organismes = self._attach_to_closest_kept_ancestor(
                deduped_organismes, ancestors
            )

        logger.info(
            "Cleaned %d raw organismes into %d organismes (%d after SIRET dedup) "
            "for referentiel %s",
            total_raw,
            total_cleaned,
            len(deduped_organismes),
            referentiel,
        )
        if referentiel == OrganismeReferentiel.DILA:
            logger.info(
                "%d DILA services not imported (no reliable SIRET, excluded, or "
                "SIRET already held by a service higher in the hierarchy)",
                total_raw - len(deduped_organismes),
            )
        return deduped_organismes

    @staticmethod
    def _attach_to_closest_kept_ancestor(
        organismes: list[Organisme], ancestors: dict[UUID, list[UUID]]
    ) -> list[Organisme]:
        """Attach each organisme to its closest imported ancestor, so that a
        service which is not imported (a directorate without SIRET, a
        regrouping…) leaves no hole in the hierarchy."""
        kept_ids = {organisme.entity_id for organisme in organismes}
        attached: list[Organisme] = []
        non_direct_attachments = 0
        for organisme in organismes:
            ancestor_ids = ancestors.get(organisme.entity_id)
            if not ancestor_ids:
                attached.append(organisme)
                continue
            parent_id = next((a for a in ancestor_ids if a in kept_ids), None)
            if parent_id != ancestor_ids[0]:
                non_direct_attachments += 1
            attached.append(
                organisme
                if parent_id == organisme.parent_id
                else _with_parent(organisme, parent_id)
            )

        logger.info(
            "%d organismes attached to an ancestor other than their direct parent",
            non_direct_attachments,
        )
        return attached

    async def _resolve_missing_dila_sirets(self, raw_batch: list[RawOrganisme]) -> None:
        if self._siret_lookup_gateway is None:
            return

        found_at = datetime.now(tz=timezone.utc)
        updates: list[tuple[UUID, Optional[str], datetime]] = []
        for raw_organisme in raw_batch:
            query = self._organismes_cleaner.dila_siret_query(raw_organisme)
            if query is None:
                continue
            try:
                candidates = self._siret_lookup_gateway.search(query)
            except Exception:
                # Not cached: the lookup is retried on the next clean.
                logger.warning(
                    "DILA SIRET lookup failed for %s",
                    raw_organisme.external_id,
                    exc_info=True,
                )
                continue
            siret = self._pick_siret(raw_organisme, query, candidates)
            raw_organisme.dila_siret_found = siret
            raw_organisme.dila_siret_found_at = found_at
            updates.append((raw_organisme.id, siret, found_at))

        await self._raw_organisme_repository.mark_dila_siret_found_batch(updates)

    def _pick_siret(
        self,
        raw_organisme: RawOrganisme,
        query: str,
        candidates: list[SiretCandidate],
    ) -> str:
        """SIRET retained for a DILA service, or "" when none is reliable."""
        data = raw_organisme.data or {}
        name = (data.get("nom") or "").strip()
        type_organisme = (data.get("type_organisme") or "").strip()

        if _is_siret(query):
            # SIRET from the DILA directory: retained if its legal unit is
            # public or associative.
            if any(
                candidate.siren == query[:_SIREN_LENGTH]
                and (candidate.is_public or candidate.is_associative)
                for candidate in candidates
            ):
                logger.info(
                    "DILA SIRET %s retained for %s (source: annuaire_dila)",
                    query,
                    raw_organisme.external_id,
                )
                return query
        else:
            retained = best_candidate(name, candidates, self._dila_siret_min_score)
            source = "recherche_entreprises"
            if retained is None and type_organisme == _EMBASSY_TYPE:
                retained = next(
                    (
                        ScoredCandidate(
                            candidate, name_score(name, candidate.denomination)
                        )
                        for candidate in candidates
                        if candidate.is_public
                        and candidate.siret
                        and embassy_matches(name, candidate.denomination)
                    ),
                    None,
                )
                source = "recherche_entreprises_ambassade"
            if retained is not None and retained.candidate.siret:
                logger.info(
                    "DILA SIRET %s retained for %s (source: %s, score: %.2f)",
                    retained.candidate.siret,
                    raw_organisme.external_id,
                    source,
                    retained.score,
                )
                return retained.candidate.siret

            associative = best_associative_candidate(name, candidates)
            if associative is not None:
                # Never retained automatically: to review for the mapping.
                logger.info(
                    "Associative candidate discarded for %s (%s): %s %s (score: %.2f)",
                    raw_organisme.external_id,
                    name,
                    associative.candidate.siret,
                    associative.candidate.denomination,
                    associative.score,
                )

        self._report_siret_not_found(raw_organisme, name, type_organisme, candidates)
        return ""

    @staticmethod
    def _report_siret_not_found(
        raw_organisme: RawOrganisme,
        name: str,
        type_organisme: str,
        candidates: list[SiretCandidate],
    ) -> None:
        reason = "no_result" if not candidates else "no_candidate_retained"
        if not is_potential_employer(name, type_organisme):
            logger.info(
                "No DILA SIRET for %s (%s): %s",
                raw_organisme.external_id,
                name,
                reason,
            )
            return

        best = best_public_candidate(name, candidates)
        with sentry_sdk.new_scope() as scope:
            scope.fingerprint = _DILA_SIRET_NOT_FOUND_FINGERPRINT
            scope.set_context(
                "dila_siret",
                {
                    "external_id": raw_organisme.external_id,
                    "nom": name,
                    "type_organisme": type_organisme,
                    "reason": reason,
                    "best_candidate": best.candidate.siret if best else None,
                    "best_candidate_denomination": (
                        best.candidate.denomination if best else None
                    ),
                    "best_candidate_score": best.score if best else None,
                },
            )
            logger.error(
                "DILA SIRET not found for %s",
                name,
                exc_info=DilaSiretNotFound(
                    raw_organisme.external_id, name, type_organisme, reason
                ),
            )
