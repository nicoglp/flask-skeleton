from app.base import model as base_model


class User(base_model.BaseModel):

    def __init__(self, id=None, username=None, status=None, roles=None, jwt=None):
        super(User, self).__init__()

        self.id = id
        self.username = username
        self.jwt = jwt
        self.status = status
        self.roles = roles

    def add_role(self, role):
        self.roles.append(role)

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)

    def has_permission(self, resource, operation):
        for role in self.roles:
            if role.has_permission(resource, operation):
                return True
        return False

    def is_owner(self, document):

        return document is None or str(document.owner_id) == self.id


class Role(base_model.BaseModel):

    def __init__(self, name, permissions=None):
        super(Role, self).__init__()

        self.name = name
        self.permissions = permissions if permissions else []

    def add_permission(self, perm):
        self.permissions.append(perm)

    def has_permission(self, resource, operation):
        for perm in self.permissions:
            if perm.match(resource, operation):
                return True
        return False


class Permission(base_model.BaseModel):

    _valid_operations = 'SCRUD'

    def __init__(self,resource, operations):
        super(Permission, self).__init__()

        self.resource = resource
        self.operations = operations

    def match(self, resource, operation):
        _op = operation.upper()
        if (_op not in self._valid_operations):
            raise ValueError("%s is not a valid operation" % _op)
        return _op in self.operations and self.resource == resource


class UserModel(base_model.BaseModel):

    owner_id = None
