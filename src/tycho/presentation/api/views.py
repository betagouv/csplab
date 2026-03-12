import yaml
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# BASE_DIR = Path(__file__).resolve().parent.parent


class StaticSchemaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        with open(settings.BASE_DIR / "docs" / "openapi.yaml", encoding="utf-8") as f:
            schema = yaml.safe_load(f)
        return Response(schema)
