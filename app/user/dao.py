from app import service
from app.base import dao

from . import schema


user_dao = dao.UBiomeServiceDAO(service.config.get('AUTH_ROOT_URL'), 'users', schema.user_schema)