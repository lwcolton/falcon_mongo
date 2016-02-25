from .resource import Resource

class EmberResource(Resource):
    def list_wrapper(found_documents):
        body = {"data":[]}
        for document_attrs in found_documents:
            document_attrs["trigger-name"] = document_attrs.pop("trigger")
            document = {
                "id":document_attrs.pop("id"),
                "attributes":document_attrs,
                "type":self.ember_type
            }
            body["data"].append(document)
        return body
