import flask

from app.base import dao as base_dao
from .exception import UnauthorizedOperationException, UnauthorizedException


class BRACDAO(base_dao.SQLAlchemyDAO):

    def __init__(self, mapped_class, schema=None):
        super(BRACDAO, self).__init__(mapped_class, schema)

    def retrieve(self, id):
        user = self._get_user()
        if user:
            object = super(BRACDAO, self).retrieve(id)
            if self._check_ownership(user, object) or self._check_authorization(user, 'R'):
                return object
        raise UnauthorizedOperationException(user, self.mapped_class.__name__, 'R')

    def create(self, object):
        # user = self._get_user()
        # if user:
        #     if self._check_authorization(user, 'C'):
        #         object.owner = user
        #         return super(BRACDAO, self).create(object)
        # raise UnauthorizedOperationException(user, self.mapped_class.__name__, 'C')
        # FIXME
        return super(BRACDAO, self).create(object)

    def update(self, object):
        user = self._get_user()
        if user:
            if self._check_ownership(user, object) or self._check_authorization(user, 'U'):
                return super(BRACDAO, self).update(object)
        raise UnauthorizedOperationException(user, self.mapped_class.__name__, 'U')

    def delete(self, object):
        user = self._get_user()
        if user:
            if self._check_ownership(user, object) or self._check_authorization(user, 'D'):
                return super(BRACDAO, self).delete(object)
        raise UnauthorizedOperationException(user, self.mapped_class.__name__, 'D')

    def search(self, filter=None, page=1, per_page=20):
        user = self._get_user()
        if self._check_authorization(user, 'S'):
            return super(BRACDAO, self).find_all(filter, page, per_page)
        raise UnauthorizedOperationException(user, self.mapped_class.__name__, 'S')

    def _check_authorization(self, user, operation):
        return user.has_permission(self.mapped_class.__name__, operation)

    def _check_ownership(self, user, document):
        return user.is_owner(document)

    def _get_user(self):
        user = flask.g.get('user', None)
        if not user:
            raise UnauthorizedException()
        return user


