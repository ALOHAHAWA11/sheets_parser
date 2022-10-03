class TaskHeader:
    def __init__(self):
        self.__company = None
        self.__target = None

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, company):
        self.__company = company

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = target
