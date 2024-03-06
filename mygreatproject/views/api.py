from rest_framework import serializers
from rest_framework.response import Response

from mygreatproject.util.apiview import MyGreatProjectRequest, mygreatproject_api_view
from mygreatproject.util.response import (
    bad_input_response,
    not_found_response,
    success_response,
)


class ReverseRequestSerializer(serializers.Serializer):
    input = serializers.CharField(required=True)


class ReverseResponseSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)


def _some_condition() -> bool:
    return False


@mygreatproject_api_view(
    "POST", req=ReverseRequestSerializer, res=ReverseResponseSerializer
)
def reverse_view(request: MyGreatProjectRequest) -> Response:
    # This is present in request.validated_data because it is required=True above:
    input = request.validated_data["input"]
    if "badness" in input:
        # When you need a 400:
        return bad_input_response(
            "Please provide a valid input",
            error_fields={"input": "badness is not allowed"},
        )
    if _some_condition():
        # When you need a 404:
        return not_found_response()
    return success_response({"content": "".join(reversed(input))})
