import json

from bson.objectid import ObjectId
import cerberus
import falcon
from mongo_validator.errors import DocumentValidationError

ID_SCHEMA = {"id":{"type":"string", "empty":False}}
REQUIRED_ID_SCHEMA = {"id":{"type":"string", "empty":False}}

class Resource:
    get_param_schema = ID_SCHEMA
    def on_get(self, req, resp):
        if not self.validate_params(req, resp, self.get_param_schema):
            return False
            
        document_id = req.params.get("item_id")

        if document_id is None:
            self.list(req, resp)
        else:
            self.get(req, resp, document_id)

    def list(self, req, resp):
        found_documents = self.document.find(self.collection)
        resp.body = list(found_documents)

    def get(self, req, resp, document_id):
        document = self.collection.find_one({"_id":document_id})
        if document is None:
            resp.status = falcon.HTTP_404
            return
        document["id"] = document_id
        del document["_id"]
        resp.body = {"object":document}

    def on_post(self, req, resp):
        document = self.document(**request.context["json"])
        try:
            document.validate()
        except DocumentValidationError as document_validation_error:
            resp.status = "422 Unprocessable Entity"
            resp.body = document_validation_error.errors
            return

        self.collection.insert_one(document)
        document["id"] = str(document["_id"])
        del document["_id"]
        resp.body = {"object":dict(document)}

    delete_param_schema = REQUIRED_ID_SCHEMA
    def on_delete(self, req, resp):
        if not self.validate_params(req, resp, self.delete_param_schema):
            return False
        document_id = req.params.get("id")
        delete_result = self.collection.delete_one({"_id":ObjectId(document_id)})
        if delete_result.deleted_count < 1:
            resp.status = falcon.HTTP_204
            return False
        elif delete_result.deleted_count > 1:
            resp.status = "712 NoSQL"
            return False

    def validate_params(self, req, resp, schema):
        param_validator = cerberus.Validator(schema)
        if not param_validator.validate(req.params):
            resp.status = "422 Unprocessable Entity"
            resp.body = json.dumps(
                {
                    "errors":param_validator.errors
                }
            )
            return False
        return True
