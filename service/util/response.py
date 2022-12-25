import logging
from typing import Any, Optional, Type

from rest_framework import serializers
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class EmptyResponseWrapperSerializer(serializers.Serializer):
    """This is the wrapper serializer for all response content returned from API endpoints."""

    m = serializers.CharField(source="message", required=False, default=None)
    e = serializers.DictField(source="extra", required=False, allow_null=True)
    s = serializers.BooleanField(source="success", required=True)


def get_wrapper_serializer(
    contained: Optional[serializers.Serializer] = None,
) -> Type[serializers.Serializer]:
    """Create a new serializer type specifically for wrapping the given serializer type."""

    if contained is not None:

        class ResponseWrapperSerializer(serializers.Serializer):
            """This is the wrapper serializer for all response content returned from API endpoints."""

            m = serializers.CharField(source="message", required=False, default=None)
            s = serializers.BooleanField(source="success", required=True)
            e = serializers.DictField(source="extra", required=False, allow_null=True)
            c = contained.__class__(source="content", required=False, default=None)  # type: ignore[misc]

            class Meta:
                ref_name = contained.__class__.__name__

        return ResponseWrapperSerializer

    else:

        return EmptyResponseWrapperSerializer


def get_success_response(
    content: Optional[serializers.Serializer] = None,
    message: Optional[str] = None,
    status_code: Optional[int] = None,
) -> Response:
    """Create and return a standard formatted response indicating that a request was successful."""
    return_serializer = get_wrapper_serializer(contained=content)
    return_data: dict[str, Any] = {
        "success": True,
    }
    if message:
        return_data["message"] = message
    if content is not None:
        # This assertion is left as two lines here so we can easily place a breakpoint and inspect
        # error results when content is not valid

        is_valid = content.is_valid()
        if not is_valid:
            logger.error(
                "Invalid content being returned from response",
                extra={
                    "data": content.data,
                    "serializer": content.__class__.__name__,
                    "errors": content.errors,
                },
            )
        assert is_valid
        return_data["content"] = content.initial_data
    if status_code is None:
        if content is not None:
            status_code = 200
        else:
            status_code = 201
    return Response(
        return_serializer(return_data).data,
        status=status_code,
    )


def get_error_response(
    error_message: Optional[str] = "Your request was invalid.",
    status_code: int = 400,
    extra: Optional[dict[Any, Any]] = None,
) -> Response:
    """Create and return a standard formatted response indicating that an error occurred."""
    return_serializer = get_wrapper_serializer()
    return_data: dict[str, Any] = {
        "success": False,
    }
    if error_message:
        return_data["message"] = error_message
    if extra:
        return_data["extra"] = extra
    return Response(
        return_serializer(return_data).data,
        status=status_code,
    )


def get_response_from_success_and_err_msg(
    success: bool, err_msg: Optional[str]
) -> Response:
    """Create and return either a success or an error response based on the contents of the
    two arguments passed in.
    """
    if not success:
        return get_error_response(error_message=err_msg)
    return get_success_response()
