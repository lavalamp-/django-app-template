from django.test.client import Client
from django.urls import reverse


def test_index(user_1_client: Client) -> None:
    r = user_1_client.get(reverse("api_index"))
    assert r.status_code == 200
