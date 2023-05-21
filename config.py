import json
from utility import rdoc


class config:
    def __new__(self, path):
        return json.loads(rdoc(path))
