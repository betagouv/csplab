"""Views for candidate website."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.candidate.container_factory import create_candidate_container
from apps.candidate.infrastructure.adapters.website.forms import (
    CorpsSearchForm,
    CVUploadForm,
)

if TYPE_CHECKING:
    from django.http import HttpRequest

    from core.entities.cv_metadata import CVMetadata


class RequiresCVMixin:
    """Mixin pour les vues qui nécessitent un CV valide dans l'URL.

    Vérifie que le cv_id passé dans l'URL correspond à un CV existant en base.
    Redirige vers la page d'upload si le CV n'existe pas.
    """

    cv_required_message: str = "CV non trouvé. Veuillez uploader votre CV."
    cv_metadata: CVMetadata | None = None

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        cv_id = kwargs.get("cv_id")
        if not cv_id:
            messages.warning(request, self.cv_required_message)
            return redirect("candidate:cv_upload")

        # Vérifier que le CV existe en base
        try:
            container = create_candidate_container()
            cv_metadata_repository = container.cv_metadata_repository()
            self.cv_metadata = cv_metadata_repository.find_by_id(cv_id)

            if not self.cv_metadata:
                messages.warning(request, self.cv_required_message)
                return redirect("candidate:cv_upload")

        except Exception:
            messages.error(request, "Erreur lors de la récupération du CV.")
            return redirect("candidate:cv_upload")

        return super().dispatch(request, *args, **kwargs)

    def get_cv_data(self) -> dict:
        """Retourne les données du CV pour le contexte."""
        if self.cv_metadata:
            return {
                "name": self.cv_metadata.filename,
                "id": str(self.cv_metadata.id),
            }
        return {}


class BreadcrumbMixin:
    """Mixin to add breadcrumb data to context."""

    breadcrumb_links: list[dict] = []
    breadcrumb_current: str = ""

    def get_breadcrumb_data(self) -> dict:
        """Return breadcrumb data for dsfr_breadcrumb tag."""
        return {
            "links": self.breadcrumb_links,
            "current": self.breadcrumb_current,
        }

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["breadcrumb_data"] = self.get_breadcrumb_data()
        return context


class HomeView(TemplateView):
    """Landing page view for CSPLab."""

    template_name = "candidate/home.html"


class CVUploadView(BreadcrumbMixin, FormView):
    """View for CV upload page with Django form handling.

    Utilise ProcessUploadedCVUsecase pour traiter le CV uploadé.
    Redirige vers la page de confirmation avec le cv_id dans l'URL.
    """

    template_name = "candidate/cv_upload.html"
    form_class = CVUploadForm
    breadcrumb_current = "Recommandation de carrière"
    breadcrumb_links = []

    def form_valid(self, form):
        """Traitement du formulaire valide via ProcessUploadedCVUsecase."""
        cv_file = form.cleaned_data["cv_file"]

        try:
            # Lire le contenu du fichier
            pdf_content = cv_file.read()

            # Utiliser le usecase pour traiter le CV
            container = create_candidate_container()
            process_cv_usecase = container.process_uploaded_cv_usecase()

            cv_id = process_cv_usecase.execute(
                filename=cv_file.name,
                pdf_content=pdf_content,
            )

            # Rediriger vers la page de confirmation avec le cv_id dans l'URL
            return redirect("candidate:cv_confirmation", cv_id=cv_id)

        except Exception as e:
            # En cas d'erreur du usecase, afficher un message et renvoyer le formulaire
            messages.error(
                self.request,
                f"Erreur lors du traitement du CV : {e!s}",
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Traitement du formulaire invalide."""
        # Ajouter un message d'erreur explicite
        for _field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class CVConfirmationView(RequiresCVMixin, BreadcrumbMixin, TemplateView):
    """View for CV confirmation/processing page.

    Affiche une animation de traitement et redirige vers les résultats.
    Le cv_id est passé dans l'URL et vérifié par RequiresCVMixin.
    """

    template_name = "candidate/cv_processing.html"
    breadcrumb_current = "Analyse en cours"
    redirect_delay_seconds = 5

    @property
    def breadcrumb_links(self):
        return [
            {"url": reverse("candidate:cv_upload"), "title": "Recommandation de carrière"},
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cv_data"] = self.get_cv_data()
        return context

    def get(self, request, *args, **kwargs):
        """Ajoute le header HTTP Refresh pour redirection automatique."""
        response = super().get(request, *args, **kwargs)
        cv_id = kwargs.get("cv_id")
        redirect_url = reverse("candidate:cv_results", kwargs={"cv_id": cv_id})
        response["Refresh"] = f"{self.redirect_delay_seconds};url={redirect_url}"
        return response


class ResultatsAnalyseView(RequiresCVMixin, BreadcrumbMixin, TemplateView):
    """Vue pour la page de résultats d'analyse du CV.

    Le cv_id est passé dans l'URL et vérifié par RequiresCVMixin.
    """

    template_name = "candidate/resultats_analyse.html"
    breadcrumb_current = "Résultat de l'analyse"
    breadcrumb_links = []

    # Données mock pour les opportunités
    MOCK_OPPORTUNITES = [
        {
            "id": 1,
            "title": "Adjoint au chargé de mission transports et mobilité",
            "type": "emploi",
            "type_label": None,
            "location": "paris",
            "location_display": "Paris",
            "public_service_branch": "Fonction publique d'État",
            "branch_key": "etat",
            "category": "A",
            "recruitment_level": "Niveau de recrutement",
            "intitule_poste": "Adjoint administratif de l'état",
        },
        {
            "id": 2,
            "title": "Concours Adjoint administratif des administrations de l'État",
            "type": "concours",
            "type_label": "Concours interne",
            "location": None,
            "location_display": None,
            "public_service_branch": "Fonction publique d'État",
            "branch_key": "etat",
            "category": "A",
            "recruitment_level": "Niveau de recrutement",
            "intitule_poste": "Adjoint administratif de l'état",
        },
        {
            "id": 3,
            "title": "Chargé(e) de mission transformation numérique",
            "type": "emploi",
            "type_label": None,
            "location": "lyon",
            "location_display": "Lyon",
            "public_service_branch": "Fonction publique Territoriale",
            "branch_key": "territoriale",
            "category": "A",
            "recruitment_level": "Niveau de recrutement",
            "intitule_poste": "Chargé de mission",
        },
        {
            "id": 4,
            "title": "Infirmier en soins généraux",
            "type": "emploi",
            "type_label": None,
            "location": "marseille",
            "location_display": "Marseille",
            "public_service_branch": "Fonction publique Hospitalière",
            "branch_key": "hospitaliere",
            "category": "A",
            "recruitment_level": "Niveau de recrutement",
            "intitule_poste": "Infirmier",
        },
        {
            "id": 5,
            "title": "Concours de rédacteur territorial",
            "type": "concours",
            "type_label": "Concours externe",
            "location": None,
            "location_display": None,
            "public_service_branch": "Fonction publique Territoriale",
            "branch_key": "territoriale",
            "category": "B",
            "recruitment_level": "Niveau de recrutement",
            "intitule_poste": "Rédacteur territorial",
        },
    ]

    def get_opportunites_filtrees(self, request):
        """Filtre les opportunités selon les paramètres de la requête."""
        # Copie profonde pour éviter de muter l'original
        opportunites = [opp.copy() for opp in self.MOCK_OPPORTUNITES]

        # Filtre par localisation
        location = request.GET.get("location", "")
        if location:
            opportunites = [o for o in opportunites if o["location"] == location]

        # Filtre par catégorie
        category = request.GET.get("category", "")
        if category:
            opportunites = [o for o in opportunites if o["category"] == category]

        # Filtre par versants (peut être multiple)
        branches = request.GET.getlist("branch")
        if branches:
            opportunites = [o for o in opportunites if o["branch_key"] in branches]

        # Ajouter les URLs de détail
        for opp in opportunites:
            opp["detail_url"] = reverse("candidate:opportunite_detail", kwargs={"pk": opp["id"]})

        return opportunites

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opportunites"] = self.get_opportunites_filtrees(self.request)
        context["cv_data"] = self.get_cv_data()

        # Passer les filtres actifs pour maintenir l'état
        context["active_filters"] = {
            "location": self.request.GET.get("location", ""),
            "category": self.request.GET.get("category", ""),
            "branches": self.request.GET.getlist("branch"),
        }
        return context

    def get(self, request, *args, **kwargs):
        """Handle GET requests, with HTMX partial rendering."""
        context = self.get_context_data(**kwargs)

        # Si requête HTMX, ne renvoyer que le fragment des résultats
        if request.headers.get("HX-Request"):
            return render(
                request,
                "candidate/components/opportunite_list.html",
                context,
            )

        return render(request, self.template_name, context)


class OpportuniteDetailView(BreadcrumbMixin, TemplateView):
    """Vue pour la page de détail d'une opportunité (mock).

    TODO: Ajouter cv_id dans l'URL pour pouvoir reconstruire le lien breadcrumb.
    """

    template_name = "candidate/opportunite_detail.html"
    breadcrumb_current = ""  # Sera défini dynamiquement
    breadcrumb_links = []  # Pas de lien breadcrumb pour l'instant (nécessiterait cv_id)

    # Données mock pour une opportunité détaillée
    MOCK_OPPORTUNITE = {
        "id": 1,
        "title": "Adjoint au chargé de mission transports et mobilité",
        "type": "emploi",
        "type_label": None,
        "employer": "Préfecture de Paris",
        "location": "Paris",
        "public_service_branch": "Fonction publique d'État",
        "branch_key": "etat",
        "category": "A",
        "recruitment_level": "Niveau de recrutement",
        "intitule_poste": "Adjoint administratif de l'état",
        "description": "Cadre de direction au sein des collectivités locales, l'attaché territorial participe à l'élaboration et à la mise en œuvre des politiques publiques locales.",
        "external_url": "https://choisirleservicepublic.gouv.fr/",
    }

    def get_breadcrumb_data(self):
        """Return breadcrumb data with dynamic current title."""
        return {
            "links": self.breadcrumb_links,
            "current": self.MOCK_OPPORTUNITE["title"][:30] + "..."
            if len(self.MOCK_OPPORTUNITE["title"]) > 30
            else self.MOCK_OPPORTUNITE["title"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # En production, on récupérerait l'opportunité par son ID
        # opportunite_id = kwargs.get("pk")
        context["opportunite"] = self.MOCK_OPPORTUNITE
        return context


class CorpsSearchView(View):
    """View for Corps semantic search."""

    template_name = "candidate/search.html"

    def get(self, request):
        """Display search form."""
        form = CorpsSearchForm()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "query": "",
                "corps_with_scores": [],
            },
        )

    def post(self, request):
        """Handle search form submission."""
        form = CorpsSearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["query"]
            limit = form.cleaned_data.get("limit", 10)

            try:
                container = create_candidate_container()
                retrieve_usecase = container.retrieve_corps_usecase()
                logger = container.logger_service()

                logger.info(f"Starting search for '{query}' with limit {limit}")
                corps_with_scores = retrieve_usecase.execute(query, limit)
                logger.info(f"Search completed, found {len(corps_with_scores)} results")

                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "query": query,
                        "corps_with_scores": corps_with_scores,
                    },
                )

            except Exception as e:
                messages.error(request, f"Erreur lors de la recherche : {e!s}")
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "query": query,
                        "corps_with_scores": [],
                    },
                )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "query": "",
                "corps_with_scores": [],
            },
        )
