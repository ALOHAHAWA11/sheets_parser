import json

from sheets_api.Task import Task
from sheets_api.TaskHeader import TaskHeader


class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            return {
                "task": obj.task_name,
                "time": obj.time,
                "subtasks": obj.sub_tasks,
                "description": obj.description
            }
        return json.JSONEncoder.default(self, obj)


class TaskHeaderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TaskHeader):
            return {
                "company": obj.company,
                "target": obj.target
            }
        return json.JSONEncoder.default(self, obj)
