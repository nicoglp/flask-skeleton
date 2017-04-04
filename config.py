import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask Configurations
THREADS_PER_PAGE = 8
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"  # TODO: configure a valid value
SECRET_KEY = "secret"
SQLALCHEMY_TRACK_MODIFICATIONS=False

# uBiome Auth config
UBIOME_AUTH_HEADER = "Authorization"
UBIOME_REQUEST_HEADER = 'X-Request-ID'
JWT_SECRET = "09Y39$%*yDm1"
AUTH_ROOT_URL = "https://apps-staging.ubiome.com/auth"

# API general config
API_PREFIX = "/api/v1"
DEBUG = "True"
SOCKET_UNIX = "/tmp/ubiome-orders-api_fcgi.sock"

# SQL Storage configuration
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/ubiome"
DATABASE_SCHEMA='kits'

# Logger configuration
JSON_LOGGING_LOCATION = "/tmp/service_json.log"
TEXT_LOGGING_LOCATION = "/tmp/service.log"
LOGGING_LEVEL = "DEBUG"

HEARTBEAT_FILE="/tmp/heartbeat.txt"
