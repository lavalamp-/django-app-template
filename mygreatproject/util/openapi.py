from typing import Any

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class MyGreatProjectOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    pass


# One of these gets created for each view+method combination:
class MyGreatProjectAutoSchema(SwaggerAutoSchema):
    def get_operation_id(self, operation_keys: Any) -> str:
        result = super().get_operation_id(operation_keys)

        # some of the POST /foo/bar/create stuff have CreateCreate, UpdateUpdate, etc.
        return (
            result.replace("_create_create", "_create")
            .replace("_update_update", "_update")
            .replace("_delete_delete", "_delete")
        )


schema_info = openapi.Info(
    title=settings.SWAGGER_SCHEMA_TITLE,
    default_version=settings.SWAGGER_SCHEMA_VERSION,
    description=settings.SWAGGER_SCHEMA_DESCRIPTION,
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@localhost"),
    license=openapi.License(name="BSD License"),
)
schema_view = get_schema_view(
    schema_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)
