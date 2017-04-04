
import flask
from werkzeug import exceptions
from app import service


@service.errorhandler(Exception)
def handle_service_error(e):
    service.logger.exception(e.message)
    _audit_after_exception(e, status=500)
    return flask.jsonify(message='The server encountered an internal error and was unable to complete your request'), 500


class ServiceException(Exception):

    def __init__(self, message):
        super(ServiceException, self).__init__()
        self.message = message

    def __str__(self):
        return repr('Service exception - {}'.format(self.message))


@service.errorhandler(ServiceException)
def handle_service_error(e):
    service.logger.exception(e.message)
    _audit_after_exception(e, exceptions.InternalServerError.__dict__['code'])
    raise exceptions.InternalServerError(description=e.message)


class InvalidDataException(ServiceException):

    def __init__(self, entity_id, entity_dict, errors):
        super(ServiceException, self).__init__('Entity data is not valid')
        self.entity_id = entity_id
        self.entity = entity_dict
        self.errors = errors

    def to_dict(self):
        return dict(message = self.message, id = self.entity_id, errors = self.errors)

    def __str__(self):
        return repr('Invalid Data Exception - {} - {}'.format(self.entity_id, self.errors))

@service.errorhandler(InvalidDataException)
def handle_service_error(e):
    log_message = 'Data is not valid for entity {} - {}'.format(e.entity_id, e.errors)
    service.logger.error(log_message, extra=dict(error='entity_deserialization_error', document_id=e.entity_id))

    return flask.jsonify(e.to_dict()), 422


class ValidationError(ServiceException):

    def __init__(self, errors=None, warnings=None):
        super(ValidationError, self).__init__("Validation errors")
        self.warnings = warnings if warnings else []
        self.errors = errors if errors else []


@service.errorhandler(ValidationError)
def handle_validation_error(e):
    service.logger.warn(e.__dict__)
    _audit_after_exception(e, 400)
    return flask.jsonify(e.__dict__), 400


class EntityNotFoundError(ServiceException):

    def __init__(self, id):
        super(EntityNotFoundError, self).__init__("Entity with id {} does not exist".format(id))
        self.id = id


@service.errorhandler(EntityNotFoundError)
def handle_validation_error(e):
    service.logger.warn(e.__dict__)
    _audit_after_exception(e, 404)
    raise exceptions.NotFound(e.message)


def _audit_after_exception(exception, status=None):

    response_msg = dict(
        endpoint=flask.request.endpoint,
        isXhr=flask.request.is_xhr,
        scheme=flask.request.scheme,
        host=flask.request.host,
        path=flask.request.path,
        method=flask.request.method,
        status=status,
        exception=exception.message
    )

    if hasattr(hasattr(response_msg,'headers'), 'Authorization'):
        del response_msg['headers']['Authorization']

    service.logger.info('{} - {}'.format (response_msg['endpoint'], response_msg['method']), extra=response_msg)
