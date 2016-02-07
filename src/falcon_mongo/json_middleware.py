import json

import falcon

class JSONMiddleware:
    def process_resource(self, req, resp, resource):
        if req.method not in ["PUT", "POST"]:
            if not getattr(resource, "process_json", False):
                return
        if getattr(resource, "process_json", True):
            if "application/json" not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                        "This API only supports requests encoded as JSON.  "
                        "You may need to set the Content-Type header to application/json"
                )
            request_body_text = req.stream.read().decode("utf-8")
            req.context["json"] = json.loads(request_body_text)

    def process_response(self, req, resp, resource):
        if req.method not in ["GET", "PUT", "POST"]:
            if not getattr(resource, "process_json", False):
                return
        if getattr(resource, "process_json", True):
            resp.body = json.dumps(resp.body)
            resp.set_header("Content-Type", "application/json")
