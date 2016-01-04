from falcon import API as FalconAPI

from .json_middleware import JSONMiddleware

class API(FalconAPI):
    def __init__(self, *args, middleware=[JSONMiddleware()], **kwargs):
        super().__init__(args, middleware=middleware, **kwargs)
