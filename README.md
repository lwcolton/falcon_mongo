# falcon_mongo

A Python 3 framework for HTTP API's with mongodb, falcon, and mongo_validator (https://github.com/lwcolton/python-mongo-validator)

Example:

```python
from falcon_mongo.api import API
from falcon_mongo.resource import Resource
from mongo_validator.document import Document
from mongo_validator import fields

class Pet(Document):
    name = fields.StringField(required=True, empty=False)
    type = fields.StringField(required=True, allowed=["cat", "dog"]
    notes = fields.StringField()

class PetResource(Resource):
    document = Pet

api = falcon_mongo.API()
api.add_route("/pets", PetResource())

