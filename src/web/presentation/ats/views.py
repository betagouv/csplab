from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def base(request):
    return render(
        request,
        "ats/base.html",
        {
            "debug": settings.DEBUG,
        },
    )
