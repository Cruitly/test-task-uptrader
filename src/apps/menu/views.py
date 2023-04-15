from typing import Optional

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def index(request: HttpRequest, menu_slug: Optional[str] = None) -> HttpResponse:
    return render(request, 'menu/index.html', context={'menu': menu_slug})
