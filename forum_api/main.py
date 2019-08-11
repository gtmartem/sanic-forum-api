from sanic import Sanic

from forum_api.api.api_versions import api_versions


if __name__ == "__main__":

    web_app = Sanic()
    web_app.blueprint(api_versions)
    web_app.run(host="0.0.0.0", port=8080, debug=True)
