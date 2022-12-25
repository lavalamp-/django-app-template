from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response

from service.util.apiview import service_api_view_empty
from service.util.response import get_success_response


class IndexResponseSerializer(serializers.Serializer):
    """Response serializer for the dummy index handler."""

    content = serializers.CharField(required=True)


@service_api_view_empty(IndexResponseSerializer, ["GET"])
def index(request: Request) -> Response:
    return get_success_response(
        content=IndexResponseSerializer(data={"content": "Hello World"})
    )
