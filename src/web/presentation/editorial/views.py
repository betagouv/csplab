from django.http import HttpResponse, HttpResponseNotFound
from django.views import View

from presentation.editorial.models import StoredFile


class ServeFileView(View):
    def get(self, request):
        stored_file = StoredFile.objects.filter(
            name=request.GET.get("name", "")
        ).first()
        if stored_file is None:
            return HttpResponseNotFound()
        response = HttpResponse(
            bytes(stored_file.content), content_type=stored_file.content_type
        )
        response["Cache-Control"] = "public, max-age=3600"
        return response
