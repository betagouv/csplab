import gzip
import io
import re
from datetime import datetime
from typing import TYPE_CHECKING, Iterator

import httpx
import ijson

from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.value_objects.organisme import OrganismeData, OrganismeImportResource
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.exceptions.exceptions import ExternalApiError

if TYPE_CHECKING:
    from _typeshed import WriteableBuffer

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


class FinessOrganismeGateway(IOrganismeGateway):
    def __init__(self, timeout: int = 300):
        self.timeout = timeout

    def find_resource(self) -> OrganismeImportResource:
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
    ) -> Iterator[OrganismeData]:
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
                        yield from self._extract_organismes(pmej)
        except httpx.HTTPError as err:
            raise ExternalApiError(
                "Erreur lors du téléchargement du fichier FINESS",
                details={"url": resource.url, "error": str(err)},
            ) from err

    @staticmethod
    def _extract_organismes(pmej: dict) -> Iterator[OrganismeData]:
        for ege in pmej.get("ege") or []:
            infos = ege.get("informationsGeneralesEGE") or {}
            numero_finess = infos.get("numFinessEge")
            if not numero_finess:
                continue
            if ege.get("etatObjet") != "A":
                continue
            ege_id = infos.get("egeId")
            roles_ege = ege.get("roleEge") or []
            if not any(role.get("idEgePorteuse") == ege_id for role in roles_ege):
                continue
            yield OrganismeData(
                referentiel=OrganismeReferentiel.FINESS,
                external_id=numero_finess,
                data=ege,
            )
