from sanic import Sanic
from sanic.exceptions import InvalidUsage, ServerError, NotFound

from forum_api.api.api_versions import api_versions
from forum_api.errors.handler import error_handler

if __name__ == "__main__":

    app = Sanic()
    app.blueprint(api_versions)
    app.error_handler.add(InvalidUsage, error_handler)
    app.error_handler.add(NotFound, error_handler)
    app.error_handler.add(ServerError, error_handler)
    app.run(host="0.0.0.0", port=8081, debug=True)
