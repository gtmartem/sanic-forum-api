import pytest

from forum_api.main import app


@pytest.mark.parametrize("url", [("/api/v5/sections",),
                                 ("/api/v5/sections/",), ])
def test_get_sections(url):
    res = app.test_client.get(url)
    request, response = res
    if url == "/api/v5/sections":
        assert response.status == 200
    if url == "/api/v5/sections/":
        assert response.status == 404
