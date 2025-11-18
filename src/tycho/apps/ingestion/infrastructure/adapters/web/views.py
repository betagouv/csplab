"""Views for ingestion API endpoints."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.sourcing.corps_sourcer import CorpsSourcer


class CorpsETLView(APIView):
    """API endpoint pour déclencher l'ETL des corps."""

    def post(self, request):
        """Trigger corps ETL process."""
        try:
            sourcer = CorpsSourcer()
            count = sourcer.fetch_and_store_corps()

            return Response(
                {
                    "status": "success",
                    "corps_created": count,
                    "message": f"{count} nouveaux corps ingérés",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
