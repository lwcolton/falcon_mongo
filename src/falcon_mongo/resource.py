class Resource:
    get_param_schema = {"id":{"type":"string", "empty":False}}
    def on_get(self, req, resp):
        param_validator = cerberus.Validator(self.get_param_schema)
        if not param_validator.validate(req.params):
            resp.status = "422 Unprocessable Entity"
            resp.body = json.dumps(
                {
                    "errors":param_validator.errors
                }
            )
            return
            
        document_id = req.params.get("item_id")
        if document_id is None:
            self.list(req, resp)
        else:
            self.get(req, resp, document_id)

    def get(self, req, resp, document_id):
        document = self.collection.find_one({"_id":document_id})
        if document is None:
            resp.status = falcon.HTTP_404
            return
        document["id"] = document_id
        del document["_id"]
        resp.body = json.dumps({"object":document})

    def on_post(self, req, resp):
        if "application/json" not in req.content_type:
            raise falcon.HTTPUnsupportedMediaType(
                    "This API only supports requests encoded as JSON.  "
                    "You may need to set the Content-Type header to application/json"
            )
        request_body_text = req.stream.read().decode("utf-8")
        request_body_dict = json.loads(request_body_text)
        document = self.document(**request_body_dict)
        try:
            document.validate()
        except DocumentValidationError as document_validation_error:
            resp.status = "422 Unprocessable Entity"
            resp.body = json.dumps(document_validation_error.errors)
            return

        self.collection.insert_one(document)
        document["id"] = str(document["_id"])
        del document["_id"]
        resp.body = json.dumps({"object":dict(document)})

    def list(self, req, resp):
        found_documents = self.document.find(self.collection)
        resp.body = json.dumps(list(found_documents))