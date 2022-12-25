from collections import OrderedDict
from typing import Optional

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.views import get_schema_view
from rest_framework import permissions, serializers

from service.util.response import get_wrapper_serializer


class ServiceOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    """This is a custom implementation of OpenAPISchemaGenerator that associates request and response serializers
    declared in service_api_view with the discovered views.
    """

    def create_view(self, callback, method, request=None):
        to_return = super().create_view(callback, method, request=request)
        if hasattr(callback, "_request_serializer"):
            setattr(
                to_return,
                "_request_serializer",
                getattr(callback, "_request_serializer"),
            )
        if hasattr(callback, "_response_serializer"):
            setattr(
                to_return,
                "_response_serializer",
                getattr(callback, "_response_serializer"),
            )
        return to_return


class ServiceAutoSchema(SwaggerAutoSchema):
    """This is a custom AutoSchema variant that is populated using the service_api_view wrapper."""

    field_inspectors = swagger_settings.DEFAULT_FIELD_INSPECTORS

    def get_request_serializer(self) -> Optional[serializers.Serializer]:
        if self.method == "GET":
            return None
        to_return = getattr(self.view, "_request_serializer", None)
        return to_return() if to_return is not None else None

    def get_query_serializer(self) -> Optional[serializers.Serializer]:
        if self.method != "GET":
            return None
        to_return = getattr(self.view, "_request_serializer", None)
        return to_return() if to_return is not None else None

    def get_response_serializers(self) -> OrderedDict[str, serializers.Serializer]:
        return_serializer = getattr(self.view, "_response_serializer", None)
        no_content_serializer = get_wrapper_serializer()()
        if return_serializer is None:
            return OrderedDict(
                {
                    "201": no_content_serializer,
                    "400": no_content_serializer,
                }
            )
        else:
            content_serializer = get_wrapper_serializer(contained=return_serializer())()
            return OrderedDict(
                {
                    "200": content_serializer,
                    "400": no_content_serializer,
                }
            )


schema_info = openapi.Info(
    title=settings.SWAGGER_SCHEMA_TITLE,
    default_version=settings.SWAGGER_SCHEMA_VERSION,
    description=settings.SWAGGER_SCHEMA_DESCRIPTION,
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
)
schema_view = get_schema_view(
    schema_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)
