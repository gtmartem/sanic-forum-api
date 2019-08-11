from sanic import Sanic

from forum_api.api.api_versions import api_versions
from forum_api.errors.exceptions import InvalidData, NoBody
from forum_api.errors.handler import error_handler

if __name__ == "__main__":

    app = Sanic()
    app.blueprint(api_versions)
    app.error_handler.add(InvalidData, error_handler)
    app.error_handler.add(NoBody, error_handler)
    app.run(host="0.0.0.0", port=8080, debug=True)
