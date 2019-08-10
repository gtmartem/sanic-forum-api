from sanic.response import json
from sanic import Sanic, Blueprint


api_v1 = Blueprint('api_v1', url_prefix='/v1')
api_v2 = Blueprint('api_v2', url_prefix='/v2')
api = Blueprint.group(api_v1, api_v2, url_prefix='/api')


@api_v1.route('/test')
async def api_v1_test(request):
    return json({'my': 'blueprint of api_v1'})


@api_v2.route('/test')
async def api_v2_test(request):
    return json({'my': 'blueprint of api_v2'})


async def all_api_test(request):
    resp = {
        "api_v1": request.app.url_for('api_v1.api_v1_test'),
        "api_v2": request.app.url_for('api_v2.api_v2_test')
    }
    return json(resp)


if __name__ == "__main__":

    web_app = Sanic()
    web_app.blueprint(api)
    web_app.add_route(all_api_test, '/simple')
    web_app.run(host="0.0.0.0", port=8080, debug=True)
