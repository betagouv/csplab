from dataclasses import dataclass
from uuid import UUID

from django.db.models import Aggregate, Count, Max, OuterRef, QuerySet, Subquery

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.services.get_recrutement_etapes import (
    recrutement_etapes,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.messagerie.models import (
    ConversationLectureModel,
    MessageModel,
    unread_conversations_count,
)
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel


@dataclass(frozen=True)
class ListeCandidatures:
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur: UserModel
    version: tuple

    def candidatures_et_etapes(
        self,
    ) -> tuple[QuerySet[CandidatureModel], list[EtapeModel]]:
        etapes = recrutement_etapes(
            organisme_id=self.organisme_id, recrutement_id=self.recrutement_id
        )
        candidatures = CandidatureModel.objects.by_recrutement(
            self.recrutement_id
        ).annotate(
            unread_conversations=unread_conversations_count(self.utilisateur.username)
        )
        return candidatures, etapes


def liste_candidatures(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    utilisateur: UserModel,
) -> ListeCandidatures:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_RECRUTEMENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    return ListeCandidatures(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        utilisateur=utilisateur,
        version=_version(organisme_id, recrutement_id, utilisateur),
    )


def _version(organisme_id: UUID, recrutement_id: UUID, utilisateur: UserModel) -> tuple:
    etapes = EtapeModel.objects.filter(recrutement=OuterRef("pk"))
    candidatures = CandidatureModel.objects.filter(etape__recrutement=OuterRef("pk"))
    messages = MessageModel.objects.filter(
        conversation__candidature__etape__recrutement=OuterRef("pk")
    )
    lectures = ConversationLectureModel.objects.filter(
        conversation__candidature__etape__recrutement=OuterRef("pk"),
        utilisateur=utilisateur,
    )
    version = (
        RecrutementModel.objects.active_by_id(recrutement_id)
        .filter(organisme_id=organisme_id)
        .annotate(
            nb_etapes=_per_recrutement(etapes, "recrutement", Count("pk")),
            etapes_maj=_per_recrutement(etapes, "recrutement", Max("updated_at")),
            nb_candidatures=_per_recrutement(
                candidatures, "etape__recrutement", Count("pk")
            ),
            candidatures_maj=_per_recrutement(
                candidatures, "etape__recrutement", Max("updated_at")
            ),
            dernier_message=_per_recrutement(
                messages,
                "conversation__candidature__etape__recrutement",
                Max("created_at"),
            ),
            derniere_lecture=_per_recrutement(
                lectures,
                "conversation__candidature__etape__recrutement",
                Max("read_at"),
            ),
        )
        .values_list(
            "updated_at",
            "nb_etapes",
            "etapes_maj",
            "nb_candidatures",
            "candidatures_maj",
            "dernier_message",
            "derniere_lecture",
        )
        .first()
    )
    if version is None:
        raise RecrutementInexistant(recrutement_id)
    return version


def _per_recrutement(queryset: QuerySet, recrutement: str, aggregate: Aggregate):
    return Subquery(
        queryset.order_by()
        .values(recrutement)
        .annotate(value=aggregate)
        .values("value")
    )
