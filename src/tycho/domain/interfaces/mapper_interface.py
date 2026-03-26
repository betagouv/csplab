from typing import Generic, Optional, Protocol, TypeVar

DomainType_contra = TypeVar("DomainType_contra", contravariant=True)
SpecificType_co = TypeVar("SpecificType_co", covariant=True)

SpecificType_contra = TypeVar("SpecificType_contra", contravariant=True)
DomainType_co = TypeVar("DomainType_co", covariant=True)


class IFromDomainMapper(Protocol, Generic[DomainType_contra, SpecificType_co]):
    def from_domain(
        self, domain_object: Optional[DomainType_contra]
    ) -> Optional[SpecificType_co]: ...


class IToDomainMapper(Protocol, Generic[SpecificType_contra, DomainType_co]):
    def to_domain(
        self, infrastructure_object: Optional[SpecificType_contra]
    ) -> Optional[DomainType_co]: ...
