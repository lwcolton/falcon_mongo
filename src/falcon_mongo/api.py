from falcon import API as FalconAPI

from .json_middleware import JSONMiddleware

class API(FalconAPI):
    def __init__(self, *args, middleware=None, **kwargs):
        if middleware is None:
            middleware = [JSONMiddleware()]
        elif type(middleware) == list:
            if JSONMiddleware not in middleware:
                middleware.append(JSONMiddleware())
        else:
            middleware = [middleware, JSONMiddleware()]
        super().__init__(args, middleware=middleware, **kwargs)
