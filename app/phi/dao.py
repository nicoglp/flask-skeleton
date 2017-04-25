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
        datetime_now = datetime.datetime.now(tz=pytz.utc)

        if not entity.owner_id:
            entity.owner_id = user.id

        if not entity.created_at:
            entity.created_at = datetime_now

        entity.created_by = user.id
        self._set_modified_data(entity, user.id, datetime_now)

        return super(PHIDAO, self).create(entity)

    def update(self, entity):
        user = self._get_user()
        self._set_modified_data(entity, user.id, datetime.datetime.now(tz=pytz.utc))

        return super(PHIDAO, self).update(entity)

    def _set_modified_data(self, entity, user_id, datetime_now):
        entity.modified_at = datetime_now
        entity.modified_by = user_id

    def _get_user(self):
        user = flask.g.get('user', None)
        if not user:
            raise exception.UnauthorizedException()
        return user

