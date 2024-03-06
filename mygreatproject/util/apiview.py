import functools
import inspect
import logging
from typing import Any, Callable, Literal, Type, Union, cast

import rest_framework.permissions
from django.http import QueryDict
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from mygreatproject.models.user import User
from mygreatproject.util.response import MyGreatProjectResponse, bad_input_response

ViewFunc = Callable[..., MyGreatProjectResponse]

logger = logging.getLogger(__name__)


class EmptyRequestSerializer(serializers.Serializer):
    """This is a dummy serializer for use on endpoints that do not expect any data."""


class EmptyResponseSerializer(serializers.Serializer):
    """This is a dummy serializer for use on endpoints that do not return any data."""


class MyGreatProjectRequest(Request):
    user: User
    validated_data: dict[Any, Any]

    @staticmethod
    def from_request(
        request: Request, serializer: Serializer
    ) -> "MyGreatProjectRequest":
        to_return = cast(MyGreatProjectRequest, request)
        to_return.validated_data = serializer.validated_data
        return to_return


class BaseResponseWrapperSerializer(serializers.Serializer):
    success = serializers.BooleanField(required=True)


class NotFoundResponseWrapperSerializer(BaseResponseWrapperSerializer):
    message = serializers.CharField(required=False, default="Not found")


class ErrorFieldSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    field = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


class InsufficientCreditsResponseWrapperSerializer(BaseResponseWrapperSerializer):
    message = serializers.CharField(required=True)


class BadInputResponseWrapperSerializer(BaseResponseWrapperSerializer):
    message = serializers.CharField(required=False, default="Bad input")
    error_fields = ErrorFieldSerializer(many=True, required=True)


def _create_wrapper_serializer(
    contained: serializers.Serializer | None = None,
) -> Type[serializers.Serializer]:
    if contained is not None:

        class ResponseWrapperSerializer(BaseResponseWrapperSerializer):
            content = contained(required=True)

            class Meta:
                ref_name = contained.__name__

        return ResponseWrapperSerializer

    else:
        return EmptyResponseSerializer


Method = Literal["GET", "PUT", "DELETE", "POST"]


def serializer_for_method(
    serializer: Type[Serializer] | dict[Method, Type[Serializer]],
    method: Method,
) -> Type[Serializer]:
    if isinstance(serializer, dict):
        return serializer.get(method, EmptyRequestSerializer)
    return serializer


def mygreatproject_api_view(
    http_method_names: list[Method] | Method,
    *,
    req: Type[Serializer] | dict[Method, Type[Serializer]] = EmptyRequestSerializer,
    res: Type[Serializer] = EmptyResponseSerializer,
    allow_logged_out: bool = False,
) -> Callable[[ViewFunc], ViewFunc]:
    ResponseSerializerKlass = _create_wrapper_serializer(res)
    ResponseSerializerKlass.__name__ = f"{res.__name__}Wrapper"  # fire, brah

    def _api_view_wrapper(fn: ViewFunc) -> ViewFunc:
        @functools.wraps(fn)
        def _wrapped(request: Request, *args: Any, **kwargs: Any) -> Response:
            request_serializer = serializer_for_method(req, request.method)

            data: Union[dict[Any, Any], QueryDict]
            if request.method == "GET":
                data = request.query_params
            else:
                data = request.data

            input_serializer = request_serializer(data=data)
            if not input_serializer.is_valid():
                logger.warning(
                    f"Input validation failed user={request.user.id}, errors={input_serializer.errors}"
                )
                mygreatproject_response = bad_input_response(
                    error_message="Whoops, we couldn't process the request.",
                    error_fields=(
                        [
                            {
                                "field": key or "unknown",
                                "message": (
                                    str(value[0]) if value else "Unknown error"
                                ),
                                "code": value[0].code if value else "unknown",
                            }
                            for key, value in input_serializer.errors.items()
                        ]
                        if input_serializer.errors
                        else []
                    ),
                )
            else:
                mygreatproject_response = fn(
                    MyGreatProjectRequest.from_request(
                        request=request, serializer=input_serializer
                    ),
                    *args,
                    **kwargs,
                )

            if mygreatproject_response.status == 404:
                return Response(
                    status=mygreatproject_response.status,
                    data=NotFoundResponseWrapperSerializer(
                        mygreatproject_response.content
                    ).data,
                )
            elif mygreatproject_response.status == 400:
                return Response(
                    status=mygreatproject_response.status,
                    data=BadInputResponseWrapperSerializer(
                        mygreatproject_response.content
                    ).data,
                )
            elif mygreatproject_response.status == 402:
                return Response(
                    status=mygreatproject_response.status,
                    data=InsufficientCreditsResponseWrapperSerializer(
                        mygreatproject_response.content
                    ).data,
                )
            elif not mygreatproject_response.content.success:
                return Response(
                    status=mygreatproject_response.status,
                    data=BaseResponseWrapperSerializer(mygreatproject_response).data,
                )

            return Response(
                status=mygreatproject_response.status,
                data=ResponseSerializerKlass(mygreatproject_response.content).data,
            )

        if allow_logged_out:
            _wrapped.permission_classes = [
                rest_framework.permissions.AllowAny,
            ]

        return _wrapped

    def decorator(fn: ViewFunc) -> ViewFunc:
        http_method_names_list = [
            m.upper()
            for m in (
                http_method_names
                if isinstance(http_method_names, list)
                else [http_method_names]
            )
        ]
        api_view_wrapped = _api_view_wrapper(fn)
        to_return = api_view(http_method_names_list)(api_view_wrapped)

        # Generate the input types allowed:
        sig = inspect.signature(fn)
        manual_parameters = []
        for p in list(sig.parameters.values())[1:]:
            if p.annotation == int:
                openapi_type = openapi.TYPE_INTEGER
            elif p.annotation == float:
                openapi_type = openapi.TYPE_NUMBER
            else:
                openapi_type = openapi.TYPE_STRING
            manual_parameters.append(
                openapi.Parameter(p.name, openapi.IN_PATH, type=openapi_type)
            )

        responses = {
            200: ResponseSerializerKlass(),
        }
        if req != EmptyRequestSerializer:
            # If the API has an input serializer, it might be invalid:
            responses[400] = BadInputResponseWrapperSerializer()
        if manual_parameters:
            # if the API handler has URL arguments, it might be not found:
            responses[404] = NotFoundResponseWrapperSerializer()

        if "GET" in http_method_names_list:
            query_serializer = serializer_for_method(req, "GET")
            to_return = swagger_auto_schema(
                method="GET",
                manual_parameters=manual_parameters,
                query_serializer=(
                    query_serializer()
                    if query_serializer != EmptyRequestSerializer
                    else None
                ),
                responses=responses,
            )(to_return)

        for method in ["POST", "PUT"]:
            if method in http_method_names_list:
                body_serializer = serializer_for_method(req, method)
                to_return = swagger_auto_schema(
                    method=method,
                    manual_parameters=manual_parameters,
                    request_body=(
                        body_serializer()
                        if body_serializer != EmptyRequestSerializer
                        else None
                    ),
                    responses=responses,
                )(to_return)

        if "DELETE" in http_method_names_list:
            to_return = swagger_auto_schema(
                method="DELETE",
                manual_parameters=manual_parameters,
                responses={
                    **responses,
                    200: BaseResponseWrapperSerializer(),
                },
            )(to_return)

        return to_return

    return decorator
