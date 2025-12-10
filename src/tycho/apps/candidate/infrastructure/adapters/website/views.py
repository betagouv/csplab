"""Views for candidate website."""

from django.contrib import messages
from django.shortcuts import render
from django.views import View

from apps.candidate.container_singleton import CandidateContainerSingleton
from apps.candidate.infrastructure.adapters.website.forms import CorpsSearchForm


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
                container = CandidateContainerSingleton.get_container()
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
                messages.error(request, f"Erreur lors de la recherche : {str(e)}")
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
