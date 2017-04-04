from werkzeug import exceptions
from app import service
from app.base.exception import _audit_after_exception

class UnauthorizedException(exceptions.Unauthorized):
    description = (
        'The server could not verify that you are authorized to do this operation'
    )


class UnauthorizedOperationException(UnauthorizedException):

    def __init__(self, user, entity,  operation):
        UnauthorizedException.__init__(self)
        self.user = user
        self.operation = operation
        self.entity = entity

    def __str__(self):
        return repr("Unauthorized operation {} {} (User : {})".format(self.entity, self.operation, self.user))


class UnauthorizedUserException(UnauthorizedException):

    def __init__(self, owner_id):
        UnauthorizedException.__init__(self)
        self.owner_id = owner_id

    def __str__(self):
        return repr("Unauthorized User : {}".format(self.owner_id))


@service.errorhandler(UnauthorizedException)
def handle_validation_error(e):
    service.logger.warn(e.__dict__)
    _audit_after_exception(e, 401)
    raise e