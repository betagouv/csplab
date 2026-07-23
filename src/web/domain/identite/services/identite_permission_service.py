from domain.identite.errors.organisme_permission_errors import CreationOrganismeRefusee


# TODO : refactor into a generic IdentitePermissionService fed with
# an IdentiteAction enum (mirroring OrganismeAction/_ROLES_REQUIS in recruteur)
class OrganismeCreationPermissionService:
    def verifier_autorisation(self, *, est_staff: bool) -> None:
        if not est_staff:
            raise CreationOrganismeRefusee()
