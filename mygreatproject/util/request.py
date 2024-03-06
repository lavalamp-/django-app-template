from typing import Optional

from rest_framework.request import Request


def ip_address_from_request(request: Request) -> Optional[str]:
    # Could use this when not behind Cloudflare:
    #   user_ip_header = request.META.get('HTTP_X_FORWARDED_FOR')
    #   return user_ip_header.split(',')[-1].strip()
    user_ip_header = request.META.get("HTTP_CF_CONNECTING_IP", None)  # Cloudflare
    if user_ip_header:
        return user_ip_header
    return request.META.get("REMOTE_ADDR")


def user_agent_from_request(request: Request) -> Optional[str]:
    """Attempt to retrieve the user agent from the given request."""
    return request.META.get("HTTP_USER_AGENT")
