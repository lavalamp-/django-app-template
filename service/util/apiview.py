import functools
from typing import Any, Callable, Optional, Type, Union, cast

from django.http import QueryDict
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from service.models.user import ServiceUser
from service.util.response import get_error_response

ViewFunc = Callable[..., Response]


class ServiceAugmentedRequest(Request):
    """This is a custom request class that is populated by the service_api_view."""

    user: ServiceUser
    serializer: Serializer
    validated_data: dict[Any, Any]

    @staticmethod
    def from_request(
        request: Request, serializer: Serializer
    ) -> "ServiceAugmentedRequest":
        """Create and return a new instance of this class as populated via the given
        DRF request and serializer.
        """
        to_return = cast(ServiceAugmentedRequest, request)
        to_return.serializer = serializer
        to_return.validated_data = serializer.validated_data
        return to_return


def service_api_view(
    req_serializer: Type[Serializer],
    resp_serializer: Optional[Type[Serializer]],
    http_method_names: Optional[list[str]],
) -> Callable[[ViewFunc], ViewFunc]:
    """This is a custom wrapper to the standard DRF api_view decorator that allows us to specify a serializer
    in its construction and thus remove a bunch of boilerplate related to data validation.
    """

    def _api_view_wrapper(fn: ViewFunc) -> ViewFunc:
        @functools.wraps(fn)
        def _wrapped(request: Request, *args: Any, **kwargs: Any) -> Response:
            data: Union[dict[Any, Any], QueryDict]
            if request.method == "GET":
                data = request.query_params
            else:
                data = request.data
            s = req_serializer(data=data)
            if not s.is_valid():
                return get_error_response(
                    error_message="Input validation failed.",
                    extra=s.errors,
                )
            augmented = ServiceAugmentedRequest.from_request(
                request=request, serializer=s
            )
            return fn(augmented, *args, **kwargs)

        return _wrapped

    def decorator(fn: ViewFunc) -> ViewFunc:
        api_view_wrapped = _api_view_wrapper(fn)
        to_return = api_view(http_method_names)(api_view_wrapped)
        setattr(to_return, "_request_serializer", req_serializer)
        setattr(to_return, "_response_serializer", resp_serializer)
        return to_return

    return decorator


class EmptyRequestSerializer(serializers.Serializer):
    """This is a dummy serializer for use on endpoints that do not expect any data."""


def service_api_view_empty(
    resp_serializer: Optional[Type[Serializer]] = None,
    http_method_names: Optional[list[str]] = None,
) -> Callable[[ViewFunc], ViewFunc]:
    """This is a specific implementation of service_api_view that is intended for handler endpoints that do
    not expect any input data.
    """
    return service_api_view(
        req_serializer=EmptyRequestSerializer,
        resp_serializer=resp_serializer,
        http_method_names=http_method_names,
    )
