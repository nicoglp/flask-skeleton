from app import api, cache
from app.base.resource import AbstractUBiomeResource


class CacheResource(AbstractUBiomeResource):
    __name__ = "cacheResource"

    def __init__(self, cache):
        self.cache = cache

    def clean_cache(self):
        self.cache.clear()

    def put(self):
        self._audit_before()
        self.clean_cache()
        ok_response = {"clean": "ok"}
        return self._response(ok_response, 200)


api.add_resource(CacheResource,
                 '/cache',
                 resource_class_args={cache})
