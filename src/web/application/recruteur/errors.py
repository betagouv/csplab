from ddd.application_errors import ApplicationError


class ApplicationRecruteurError(ApplicationError): ...


class ErreurPaginationQuery(ApplicationRecruteurError): ...
