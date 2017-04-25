"""
    Config of cache.
    more info: http://pythonhosted.org/Flask-Cache/
"""
SIMPLE_BACK_IMPL = "simple"


class CacheConfig():
    @staticmethod
    def get_cache_config(enviroment):
        if enviroment == SIMPLE_BACK_IMPL:
            return CacheConfig.get_simple_config();
        # default
        else:
            return CacheConfig.get_redis_config();

    @staticmethod
    def get_redis_config():
        return {'CACHE_TYPE': 'redis',
                'CACHE_KEY_PREFIX': 'flask_cache',
                'CACHE_REDIS_HOST': 'localhost',
                'CACHE_REDIS_PORT': '6379',
                'CACHE_DEFAULT_TIMEOUT': '3600',
                'CACHE_REDIS_URL': 'redis://localhost'
                }

    @staticmethod
    def get_simple_config():
        return {'CACHE_TYPE': 'simple',
                'CACHE_DEFAULT_TIMEOUT': '3600',
                'CACHE_KEY_PREFIX': 'flask_cache'
                }
