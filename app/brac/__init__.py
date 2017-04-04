import flask
from jwt import exceptions as jwt_exceptions
from werkzeug import exceptions as http_exceptions

from app import service
from app.lib import json_web_token

from app.user import dao as user_dao
from app.user import model as user_model

from . import dao
from . import exception


def require_auth(method):
    """
    Authorization decorator. Look up an HTTP Authorization header
    with the exact SECRET_SHARED_KEY.
    JWT Capabilities were added for using the JWT Token in the
    request if the traditional login system doesn't log the user
    """
    def require_auth_func(*args, **kwargs):
        token = flask.request.headers.get('Authorization')
        if token == service.config.get('SECRET_SHARED_KEY'):
            api_user_id = service.config.get('API_USER')
            user = _get_user(api_user_id)
            if not user:
                return service.response_class(
                    flask.json.dumps(dict(message="Unauthorized exception - User does not exist".format(api_user_id))),
                    mimetype='application/json',
                    status=401
                )
            flask.g.user = user
            service.logger.info("Authentication success for user {}".format(str(api_user_id)))
            return method(*args, **kwargs)
        elif not flask.g.get('user', None):
            if service.config['UBIOME_AUTH_HEADER'] in flask.request.headers:

                service.logger.debug('Authenticating user with jwt')
                try:
                    jwt_token = json_web_token.parse_jwt_oauth2(
                            flask.request.headers.get(service.config.get('UBIOME_AUTH_HEADER')))

                   # Created a temporary user in local_thread in order to use this jwt in Auth call
                    flask.g.user = user_model.User(jwt=flask.request.headers.get(service.config.get('UBIOME_AUTH_HEADER')))

                    user_id = jwt_token.get('user_id')
                    user = user_dao.user_dao.retrieve(user_id)

                    if not user:
                            service.logger.warn("Authentication failure - User does not exist".format(user_id))
                            return service.response_class(
                                flask.json.dumps(dict(message="Unauthorized exception - User does not exist".format(user_id))),
                                mimetype='application/json',
                                status=401
                            )

                    user.jwt = flask.request.headers.get(service.config.get('UBIOME_AUTH_HEADER'))
                    flask.g.user = user

                    service.logger.info("Authentication success for user '%s'" % jwt_token.get('user_id'))
                    return method(*args, **kwargs)

                except jwt_exceptions.InvalidTokenError as e:
                    service.logger.warn("Authentication failure - %s" % e.message)
                    return service.response_class(
                        flask.json.dumps(dict(message="Unauthorized exception - %s" % e.message)),
                        mimetype='application/json',
                        status=401
                    )
            else:
                service.logger.warn("Authentication failure - Authorization header not present")
                return service.response_class(
                        flask.json.dumps(dict(message=http_exceptions.Unauthorized.description)),
                        mimetype='application/json',
                        status=401
                    )
        else:
            service.logger.debug("User %s already authenticated" % flask.g.user.id)
            return method(*args, **kwargs)


    return require_auth_func

def _get_user(user_id):
    user = user_dao.user_dao.retrieve(user_id)
    if not user:
        service.logger.warn("Authentication failure - User does not exist".format(user_id))
        return None
    return user