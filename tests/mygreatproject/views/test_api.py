from django.test.client import Client
from django.urls import reverse


def test_reverse(user_1_client: Client) -> None:
    r = user_1_client.get(reverse("api_reverse"))
    assert r.status_code == 405
    r = user_1_client.post(reverse("api_reverse"), data={"input": "hello"})
    assert r.status_code == 200
    assert r.json() == {"success": True, "content": {"reversed": "olleh"}}
