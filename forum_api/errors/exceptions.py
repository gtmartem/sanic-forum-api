from sanic.exceptions import ServerError, NotFound, InvalidUsage


def server_error_wrapper(fn):
    async def wrapped(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except NotFound as nf:
            raise nf
        except InvalidUsage as iu:
            raise iu
        except Exception:
            raise ServerError("server error")
    return wrapped
