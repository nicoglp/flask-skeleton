import flask, os
from flask_restful import Api
from flask import current_app
import werkzeug.exceptions
import json
import flask_sqlalchemy

from sqlalchemy.schema import MetaData

from app.base import logger

# App Configurations
service = flask.Flask(__name__)
service.config.from_object('config')
config = service.config

# API Configuration
api = Api(service, prefix=service.config.get('API_PREFIX'))

# DB Configurations
metadata = MetaData(schema=service.config['DATABASE_SCHEMA'])
db = flask_sqlalchemy.SQLAlchemy(service, session_options=dict(autocommit=False, autoflush=False), metadata=metadata)

logger.config_logger(service)


# Map all docs files into /docs URL if the Environment is not production
if os.environ.get("UBIOME_ENVIRONMENT") is not 'production':
    # Avoid warnings for urllib3
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()

    # Map all docs files into /docs URL
    @service.route('/docs/<path:path>')
    def send_doc(path):
        return flask.send_from_directory(current_app.root_path + '/static/docs', path, mimetype='text/yaml')


# Heartbeat service
@service.route('/heartbeat')
def heartbeat():
    try:
        if open(service.config.get('HEARTBEAT_FILE'), 'r'):
            return service.response_class(
                status=200)
    except Exception as e:
        service.logger.error('Error in heartbeat endpoint with error %s ' % e.message)
        return service.response_class(
            status=500)


@service.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(error):
    if error.data is not None:
        return json.dumps(error.data.get('message'))
    else:
        return error


@service.after_request
def cores_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Accept,Content-Type,Authorization,X-Request-ID')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response


# Load resources
from app.ping import resource
from app.kits import resource
