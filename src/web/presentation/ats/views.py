import json

from django.conf import settings
from django.shortcuts import render


def base(request):
    user_data = {"is_authenticated": request.user.is_authenticated}
    if request.user.is_authenticated:
        user_data["email"] = request.user.email

    return render(
        request,
        "ats/base.html",
        {
            "debug": settings.DEBUG,
            "user_json": json.dumps(user_data),
        },
    )
