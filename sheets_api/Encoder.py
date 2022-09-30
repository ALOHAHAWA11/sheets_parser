import json

from sheets_api.Task import Task


class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
