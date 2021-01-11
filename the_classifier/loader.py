import json


class Loader(object):
    def process(self, path):
        with open(path) as f:
            data = [json.loads(row) for row in f]
            return data
