import flask
import flask_restful
import json, collections
from werkzeug import exceptions as http_exception

from app import service
from app.base.exception import ValidationError
from app.brac import require_auth

from . import model
from . import schema
from . import exception


class AbstractUBiomeResource(flask_restful.Resource):

    def _audit_before(self):

        request_msg = dict(
            endpoint=flask.request.endpoint,
            isXhr=flask.request.is_xhr,
            scheme=flask.request.scheme,
            host=flask.request.host,
            app=flask.request.script_root,
            path=flask.request.path,
            method=flask.request.method,

            values=flask.request.values.to_dict(),
            headers=dict(flask.request.headers.items()),
        )
        if 'Authorization' in request_msg['headers']:
            del request_msg['headers']['Authorization']

        service.logger.info('{} - {}'.format(request_msg['endpoint'], request_msg['method']), extra=request_msg)

    def _audit_after(self, response, status=None):

        try:
            message = json.loads(response.data).get('id')
        except Exception as e:
            message = None


        response_msg = dict(
            endpoint=flask.request.endpoint,
            isXhr=flask.request.is_xhr,
            scheme=flask.request.scheme,
            host=flask.request.host,
            path=flask.request.path,
            method=flask.request.method,
            status = status,
            document_id=message,
            mimetype = response.mimetype,
            headers = dict(response.headers.items())
        )

        if hasattr(response_msg['headers'], 'Authorization'):
            del response_msg['headers']['Authorization']

        service.logger.info('{} - {}'.format(response_msg['endpoint'], response_msg['method']), extra=response_msg)

    def _response(self, response, status, mimetype='application/json'):

        response = service.response_class(
            flask.json.dumps(response),
            mimetype=mimetype,
            status=status
        )
        self._audit_after(response, status)
        return response


class BaseResource(AbstractUBiomeResource):

    def __init__(self, dao, schema, validators=None):
        self.validators = validators if validators else []
        self.dao = dao
        self.schema = schema

    def validate(self, entity, **kwargs):
        errors = []
        for v in self.validators:
            valid, error = v.execute(entity, **kwargs)
            if not valid:
                formatted_error = "{{ {} }}".format(error)
                errors.append(formatted_error)
        if errors:
            raise exception.ValidationError(errors="[{}]".format(",".join(errors)))


class EntityResource(BaseResource):
    """
    Support to basic REST operations over specific entity.
    """

    def __init__(self, dao, schema, validators):
        BaseResource.__init__(self, dao, schema, validators)

    def get(self, id, **kwargs):
        self._audit_before()

        entity = self.dao.retrieve(id)
        if entity:
            response, errors = self.schema.dump(entity)
            return self._response(response, 200)
        else:
            raise exception.EntityNotFoundError(id)

    def post(self, id, **kwargs):
        self._audit_before()

        entity = self.dao.retrieve(id)
        if entity:
            raise http_exception.Conflict(description = 'Entity already exist')
        else:
            raise exception.EntityNotFoundError(id)

    def put(self, id, **kwargs):
        self._audit_before()

        entity, errors = self.schema.load(flask.request.get_json())
        if len(errors) > 0:
            raise exception.ValidationError(errors=errors)

        entity.id = id

        self.validate(entity=entity)

        with self.dao.session_scope():
            updated_entity = self.dao.update(entity)
            service.logger.info(
                    "Entity {} has been updated".format(updated_entity.id),
                    extra=dict(document_id=str(updated_entity.id)))
            response, errors = self.schema.dump(updated_entity)
            return self._response(response, 200)

    def patch(self, id, **kwargs):

        self._audit_before()

        entity = self.dao.retrieve(id)
        if entity:
            self.validate(entity=entity)
            patch_dict = flask.request.get_json()
            with self.dao.session_scope():
                updated_entity = self.dao.patch(entity, patch_dict)
                service.logger.info(
                    "Entity {} has been patched".format(updated_entity.id),
                    extra=dict(document_id=str(updated_entity.id)))
                response, errors = self.schema.dump(updated_entity)
                return self._response(response, 200)

        else:
            raise exception.EntityNotFoundError(id)


    def delete(self, id, **kwargs):
        self._audit_before()
        entity = self.dao.retrieve(id)
        with self.dao.session_scope():
            if entity:
                deleted_entity = self.dao.delete(entity)
                if deleted_entity:
                    response, errors = self.schema.dump(deleted_entity)
                    service.logger.info(
                    "Entity {} has been deleted".format(id),
                        extra=dict(document_id=id))
                    return self._response(response, 200)

            raise exception.EntityNotFoundError(id)


class CollectionResource(BaseResource):
    """
    Support to basic REST operations over entity's collections.
    """

    def __init__(self, dao, schema, validators=None):
        BaseResource.__init__(self, dao, schema, validators)

    def get(self, **kwargs):
        self._audit_before()

        per_page = flask.request.args.get('pageSize', 20, type=int)
        page = flask.request.args.get('pageNumber', 1, type=int)

        pagination = self.dao.find_all(page=page, per_page=per_page)

        pages, page_errors = schema.pagination_schema.dump(pagination)
        data, data_errors = self.schema.dump(pagination.items, many=True)
        return self._response(dict(items=data,page=pages), 200)

    def post(self, **kwargs):
        self._audit_before()

        entity, errors = self.schema.load(flask.request.get_json())
        if len(errors) > 0:
            raise exception.ValidationError(errors=errors)

        self.validate(entity=entity)

        with self.dao.session_scope():
            created_entity = self.dao.create(entity)
            service.logger.info("Entity {} has been created".format(created_entity.id),
                                extra=dict(document_id=str(created_entity.id)))
            response, errors = self.schema.dump(created_entity)
            return self._response(response, 201)

    def put(self, **kwargs):
        self._audit_before()

        raise http_exception.MethodNotAllowed(description='Unable to update/replace every resource in the entire collection')

    def patch(self, **kwargs):
        self._audit_before()

        raise http_exception.MethodNotAllowed(description='Unable to update/replace every resource in the entire collection')

    def delete(self, **kwargs):
        self._audit_before()

        return http_exception.MethodNotAllowed(description='Unable to delete the whole collection')


class SearchResource(BaseResource):
    """
    Support search operation over entity's collections.
    """

    def __init__(self, dao, schema):
        BaseResource.__init__(self, dao, schema)

    def post(self):
        self._audit_before()

        per_page = flask.request.args.get('pageSize', 20, type=int)
        page = flask.request.args.get('pageNumber', 1, type=int)

        payload = flask.request.get_json()
        if not payload or 'filter'not in payload:
            raise schema.FilterError(errors=dict(filter="You must specify a filter"))

        find = model.Find()
        find.filters = schema.parse_filter(payload.get('filter',{}))
        find.sort = schema.parse_order(payload.get('order', {}))

        pagination = self.dao.search(find, page=page, per_page=per_page)

        pages, page_errors = schema.pagination_schema.dump(pagination)
        data, data_errors = self.schema.dump(pagination.items, many=True)
        return self._response(dict(items=data, page=pages), 200)


class CheckResource(BaseResource):

    @require_auth
    def get(self):
        self._audit_before()

        json_errors = []
        per_page=100

        page = self.dao.find_all(page=1, per_page=per_page)
        json_errors.extend([e.to_dict() for e in page.invalid_data])

        while page.has_next:
            page = self.dao.find_all(page=page.next_num, per_page=per_page)
            json_errors.extend([e.to_dict() for e in page.invalid_data])

        service.logger.info('{} entities has been checked with {} errors.'.format(page.total, len(json_errors)))

        return self._response(dict(page={"total": page.total, "errors":len(json_errors)}, items=json_errors), 200)
