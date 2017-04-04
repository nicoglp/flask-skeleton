from app import service
from app.base import resource as base_resources
from app.brac import require_auth

from . import schema

class PingResource(base_resources.BaseResource):
    """
    This class represents the resource which you can check the service status
    """
    def __init__(self, healt_check):
        super(PingResource, self).__init__(None, schema.health_result)
        self.healt_check = healt_check

    @require_auth
    def get(self):
        """
        Check the service
        """
        service.logger.info('::Ping endpoint::')

        results, errors = self.schema.dump(self.healt_check.check(), many=True)

        return self._response(results)
