import datetime
import flask
import pytz

from app.brac.dao import BRACDAO
from app.brac import exception


class PHIDAO(BRACDAO):

    def __init__(self, mapped_class, schema=None):
        super(PHIDAO, self).__init__(mapped_class, schema)

    def create(self, entity):
        user = self._get_user()

        if not entity.owner_id:
            entity.owner_id = user.id

        if not entity.created_at:
            entity.created_at = datetime.datetime.now(tz=pytz.utc)

        entity.modified_at = datetime.datetime.now(tz=pytz.utc)
        entity.modified_by = user.id

        return super(PHIDAO, self).create(entity)

    def update(self, entity):
        user = self._get_user()
        entity.modified_at = datetime.datetime.now(tz=pytz.utc)
        entity.modified_by = user.id

        return super(PHIDAO, self).update(entity)

    def _get_user(self):
        user = flask.g.get('user', None)
        if not user:
            raise exception.UnauthorizedException()
        return user

