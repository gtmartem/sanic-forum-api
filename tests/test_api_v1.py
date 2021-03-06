import pytest
from sanic.testing import SanicTestClient

from forum_api.main import app


@pytest.mark.parametrize(("url",), [("/api/v1/sections",),
                                    ("/api/v1/sections/",),
                                    ("/api/v1/sevtions",), ])
def test_get_sections(url):
    res = SanicTestClient(app, port="8080").get(url)
    request, response = res
    if url in ["/api/v1/sections", "/api/v1/sections/"]:
        assert response.status == 200
    if url == "/api/v1/sevtions":
        assert response.status == 404


@pytest.mark.parametrize(("url",), [("/api/v1/sections/1",),
                                    ("/api/v1/sections/0",),
                                    ("/api/v1/sections/abc",),
                                    ("/api/v1/sevtions/5",),
                                    ("/api/v1/sevtions/",), ])
def test_get_sections_by_page(url):
    res = SanicTestClient(app, port="8080").get(url)
    request, response = res
    if url in ["/api/v1/sections/1",
               "/api/v1/sections/0"]:
        assert response.status == 200
    if url in ["/api/v1/sections/abc",
               "/api/v1/sevtions/5",
               "/api/v1/sevtions/"]:
        assert response.status in (404, 400)
