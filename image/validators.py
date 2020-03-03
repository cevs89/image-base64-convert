from cerberus import Validator
from image.models import STATUS_CHOICE


class ImageCreateValidator():
    """
    {
        "model": cooler/poster,
        "picture": <base 64>,
        "image_analysis_id": aphanumber,
        "transaction_status": Complete/In Progress/Failed,
    }

    """

    schema = {
        "model": {
            "type": "string",
            'allowed': [name for name in ["cooler", "poster"]],
        },
        "picture": {
            "type": "string",
        },
        "image_analysis_id": {
            "type": "string",
        },
        "transaction_status": {
            "type": "string",
            'allowed': [i[1] for i in STATUS_CHOICE],
        },
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors
