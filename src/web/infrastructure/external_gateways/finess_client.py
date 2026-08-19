import gzip
import io
import re
from datetime import datetime
from typing import TYPE_CHECKING, Iterator

import httpx
import ijson
from ddd.mapper_interface import IToDomainMapper
from ddd.services.logger_interface import ILogger
from referentiel.value_objects.department import Department

if TYPE_CHECKING:
    from _typeshed import WriteableBuffer

from domain.identite.entities.organisme import Organisme
from domain.identite.gateways.organisme_gateway_interface import (
    IOrganismeGateway,
    OrganismeImportResource,
)
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dtos.finess_dtos import EtablissementDTO

DATASET_API_URL = "https://www.data.gouv.fr/api/1/datasets/finess-structures-1/"
JOURNALIER_TITLE_PATTERN = re.compile(
    r"^finess-structures-journalier-(\d{8})\.json\.gz$"
)


class _ChunkedBinaryStream(io.RawIOBase):
    """Adapts an httpx streamed byte-chunk iterator into a readable binary
    stream, so the gzip payload can be decompressed without buffering the
    whole (multi-hundred-MB) response in memory."""

    def __init__(self, chunks: Iterator[bytes]):
        self._chunks = chunks
        self._leftover = b""

    def readable(self) -> bool:
        return True

    def readinto(self, buffer: "WriteableBuffer") -> int:
        if not self._leftover:
            try:
                self._leftover = next(self._chunks)
            except StopIteration:
                return 0
        view = memoryview(buffer)  # type: ignore[arg-type]
        chunk, self._leftover = (
            self._leftover[: len(view)],
            self._leftover[len(view) :],
        )
        view[: len(chunk)] = chunk
        return len(chunk)


class FinessClient(IOrganismeGateway):
    def __init__(
        self,
        logger: ILogger,
        organisme_mapper: IToDomainMapper[EtablissementDTO, Organisme],
        timeout: int = 300,
    ):
        self.logger = logger
        self.organisme_mapper = organisme_mapper
        self.timeout = timeout

    def find_latest_resource(self) -> OrganismeImportResource:
        try:
            response = httpx.get(DATASET_API_URL, timeout=30)
            response.raise_for_status()
        except httpx.HTTPError as err:
            raise ExternalApiError(
                "Impossible de récupérer le dataset FINESS",
                details={"url": DATASET_API_URL, "error": str(err)},
            ) from err

        candidates = []
        for resource in response.json().get("resources", []):
            match = JOURNALIER_TITLE_PATTERN.match(resource.get("title") or "")
            if match and resource.get("url"):
                millesime = datetime.strptime(match.group(1), "%Y%m%d").date()
                candidates.append(
                    OrganismeImportResource(url=resource["url"], millesime=millesime)
                )

        if not candidates:
            raise ExternalApiError(
                "Aucun fichier FINESS journalier trouvé dans le dataset",
                details={"url": DATASET_API_URL},
            )

        return max(candidates, key=lambda candidate: candidate.millesime)

    def stream_organismes(
        self, resource: OrganismeImportResource
    ) -> Iterator[Organisme]:
        millesime = resource.millesime.isoformat()
        try:
            with httpx.stream(
                "GET", resource.url, timeout=self.timeout, follow_redirects=True
            ) as response:
                response.raise_for_status()
                binary_stream = io.BufferedReader(
                    _ChunkedBinaryStream(response.iter_bytes())
                )
                with gzip.GzipFile(fileobj=binary_stream) as gzip_stream:
                    for pmej in ijson.items(gzip_stream, "pmej.item"):
                        for dto in self._extract_etablissements(pmej, millesime):
                            yield self.organisme_mapper.to_domain(dto)
        except httpx.HTTPError as err:
            raise ExternalApiError(
                "Erreur lors du téléchargement du fichier FINESS",
                details={"url": resource.url, "error": str(err)},
            ) from err

    @staticmethod
    def _extract_etablissements(
        pmej: dict, millesime: str
    ) -> Iterator[EtablissementDTO]:
        for ege in pmej.get("ege") or []:
            infos = ege.get("informationsGeneralesEGE") or {}
            siret = infos.get("siret")
            numero_finess = infos.get("numFinessEge")
            nom = (infos.get("nomEgeLong") or infos.get("nomEgeCourt") or "").strip()
            if not siret or not numero_finess or not nom:
                continue

            latitude, longitude, departement = FinessClient._extract_localisation(ege)

            yield EtablissementDTO(
                nom=nom,
                external_id=numero_finess,
                siret=siret,
                latitude=latitude,
                longitude=longitude,
                departement=departement,
                millesime=millesime,
            )

    @staticmethod
    def _extract_localisation(
        ege: dict,
    ) -> tuple[float | None, float | None, str | None]:
        adresses = ege.get("adresse") or []
        if not adresses:
            return None, None, None

        coordonnees = adresses[0].get("coordonneesGeographique") or {}
        latitude = _to_float(coordonnees.get("coordonneeY"))
        longitude = _to_float(coordonnees.get("coordonneeX"))

        commune = adresses[0].get("cogCommune")
        department = Department.from_commune_code(commune) if commune else None

        return latitude, longitude, department.code if department else None


def _to_float(value: str | None) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None
