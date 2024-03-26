from django.http import HttpRequest, HttpResponse


def index_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello world")
