from dataclasses import dataclass


@dataclass
class ArchiveOfferByReferenceInput:
    reference: str
    source_id: str
