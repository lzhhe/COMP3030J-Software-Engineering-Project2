class User:
    def __init__(self, uid, name, password, department=None):
        self.name = name
        self.uid = uid
        self.password = password
        self.department = department


class DepartmentManager(User):
    def __int__(self, uid, name, password, department):
        super().__init__(uid, name, password, department)


class GovernmentManager(User):
    def __int__(self, uid, name, password, department=None):
        super().__init__(uid, name, password, department)


class WasteManager(User):
    def __int__(self, uid, name, password, department=None):
        super().__init__(uid, name, password, department)


class IndividualUser(User):
    def __int__(self, uid, name, password, department=None):
        super().__init__(uid, name, password, department)
