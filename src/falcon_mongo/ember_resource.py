from .resource import Resource

class EmberResource(Resource):
    def list_wrapper(self, found_documents):
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

    def get_wrapper(self, found_document):
        body = {
            "data":{
                "id":found_document.pop("id"),
                "type":self.ember_type,
                "attributes":found_document
            }
        }
        return body

