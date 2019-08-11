from sanic import Blueprint

from forum_api.api.v1.v1 import v1

api_versions = Blueprint.group([
    v1
], url_prefix="/api")