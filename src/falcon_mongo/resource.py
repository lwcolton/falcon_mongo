import json

from bson.objectid import ObjectId
import cerberus
import falcon
from mongo_validator.errors import DocumentValidationError

ID_SCHEMA = {"id":{"type":"string", "empty":False}}
REQUIRED_ID_SCHEMA = {"id":{"type":"string", "empty":False, "required":True}}

class Resource:
    get_param_schema = ID_SCHEMA
    def on_get(self, req, resp, document_id=None):
        if not self.validate_params(req, resp, self.get_param_schema):
            return False
            
        if document_id is None:
            self.list(req, resp)
        else:
            self.get(req, resp, ObjectId(document_id))

    def list(self, req, resp):
        found_documents = self.document.find(self.collection)
        resp.body = self.list_wrapper(found_documents)

    def list_wrapper(self, found_documents):
        return list(found_documents)

    def get(self, req, resp, document_id):
        document = self.document.find_one(self.collection, {"_id":document_id})
        if document is None:
            resp.status = falcon.HTTP_404
            return 
        resp.body = self.get_wrapper(document)

    def get_wrapper(self, found_document):
        return {"object":found_document}

    def on_post(self, req, resp):
        document = self.document(**req.context["json"])
        try:
            document.validate()
        except DocumentValidationError as document_validation_error:
            resp.status = "422 Unprocessable Entity"
            resp.body = {"errors":document_validation_error.errors}
            return

        self.collection.insert_one(document)
        document["id"] = str(document["_id"])
        del document["_id"]
        resp.body = self.create_wrapper(document)

    def create_wrapper(self, document):
        return {"object":dict(document)}

    put_param_schema = REQUIRED_ID_SCHEMA
    def on_put(self, req, resp):
        if not self.validate_params(req, resp, self.delete_param_schema):
            return False
        document_id = req.params.get("id")
        document = self.document.get(self.collection, document_id)
        if document is None:
            resp.status = falcon.HTTP_404
            return 
        document.update(req.context["json"])
        try:
            document.validate()
        except DocumentValidationError as document_validation_error:
            resp.status = "422 Unprocessable Entity"
            resp.body = {"errors":document_validation_error.errors}
        replace_result = self.collection.replace_one({"_id":ObjectId(document_id)}, document)
        if replace_result.matched_count == 1 and replace_result.modified_count == 1:
            return
        else:
            resp.status = "712 NoSQL"

    def on_delete(self, req, resp, document_id):
        delete_result = self.collection.delete_one({"_id":ObjectId(document_id)})
        print(delete_result)
        if delete_result.deleted_count == 1:
            resp.status = falcon.HTTP_204
            resp.body = "deleted"
            return False
        elif delete_result.deleted_count == 0:
            resp.status = falcon.HTTP_404
        else:
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
