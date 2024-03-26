import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class MyGreatProjectResponseContent:
    success: bool
    message: str | None = None
    content: dict[str, Any] | None = None
    error_fields: dict[str, Any] | None = None


@dataclass
class MyGreatProjectResponse:
    status: int
    content: MyGreatProjectResponseContent


def get_response(
    content: dict[str, Any] | None = None,
    message: str | None = None,
    status_code: int | None = None,
    error_fields: dict[str, Any] | None = None,
    success: bool = True,
) -> MyGreatProjectResponse:
    response_content = MyGreatProjectResponseContent(
        success=success,
        message=message,
        content=content,
        error_fields=error_fields,
    )
    if status_code is None:
        if content is not None:
            status_code = 200
        else:
            status_code = 201
    return MyGreatProjectResponse(
        status=status_code,
        content=response_content,
    )


def success_response(
    content: dict[str, Any] | None = None,
    message: str | None = None,
) -> MyGreatProjectResponse:
    return get_response(
        content=content,
        message=message,
    )


def deletion_ok_response() -> MyGreatProjectResponse:
    return get_response(
        message="OK",
        # NOTE: 204 causes fetch() to fail to parse json. so. no 204.
        status_code=200,
    )


def bad_input_response(
    error_message: str | None = None,
    error_fields: dict[str, Any] | None = None,
) -> MyGreatProjectResponse:
    return get_response(
        message=error_message,
        error_fields=error_fields or [],
        status_code=400,
        success=False,
    )


def not_found_response(
    message: str | None = None,
) -> MyGreatProjectResponse:
    return get_response(
        message=message,
        status_code=404,
        success=False,
    )


def unavailable_response(
    message: str | None = None,
) -> MyGreatProjectResponse:
    return get_response(
        message=message,
        status_code=503,
        success=False,
    )


def insufficient_credits_response(
    message: str | None = None,
) -> MyGreatProjectResponse:
    return get_response(
        message=message,
        status_code=402,
        success=False,
    )
