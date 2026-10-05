from ddd.domain_errors import DomainError


class DocumentError(DomainError):
    pass


class FichierDeposeIncomplet(DocumentError):
    def __init__(self):
        super().__init__("Un fichier déposé doit avoir un nom, un type et une taille")
