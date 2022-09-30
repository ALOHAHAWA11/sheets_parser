class Task:

    def __init__(self, task_name):
        self.__task_name = task_name
        self.__time = None
        self.__sub_tasks = []


    @property
    def sub_tasks(self):
        return self.__sub_tasks

    @sub_tasks.setter
    def sub_tasks(self, task):
        self.__sub_tasks = task

    @property
    def task_name(self):
        return self.__task_name

    @task_name.setter
    def task_name(self, task_name):
        self.__task_name = task_name

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time
