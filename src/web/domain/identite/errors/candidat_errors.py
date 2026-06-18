from ddd.domain_errors import DomainError


class CandidatError(DomainError):
    pass


class ProfilCandidatExisteDeja(CandidatError):
    def __init__(self, email: str):
        super().__init__(f"Candidat profile with email {email} already exists")
