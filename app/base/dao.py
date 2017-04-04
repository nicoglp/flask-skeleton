import flask
import requests
import json
import collections

from contextlib import contextmanager
from sqlalchemy.orm import base as sqla_base
from sqlalchemy import or_, desc, asc

from app import db, service
from . import schema
from . import model
from . import exception


class SQLAlchemyDAO(object):
    """
    Implement basic functionality for SQL DAOs as CRUD and transactions management.
    For transactions : http://docs.sqlalchemy.org/en/rel_0_8/orm/session.html#session-faq-whentocreate
    """
    def __init__(self, mapped_class, schema=None):
        if not sqla_base._is_mapped_class(mapped_class):
            raise exception.ServiceException('%s is not a mapped class' % mapped_class)
        self.mapped_class = mapped_class
        self.schema = schema

    def retrieve(self, id):
        return self.mapped_class.query.get(id)

    def dettach(self, object):
        db.session.expunge(object)

    def create(self, object):
        db.session.add(object)
        db.session.flush()
        return object

    def createAll(self, objects):
        db.session.bulk_save_objects(objects)
        db.session.flush()
        return object

    def update(self, object):
        updated_object = db.session.merge(object)
        db.session.flush()
        return updated_object

    def patch(self, object, patch_dict):
        patched_object = self._patch(object, patch_dict, self.schema, self.mapped_class)
        return self.update(patched_object)

    def _patch(self, obj, patch_dict, schema, mapped_class):
        """
        Deep model update using a dictionary.
        Dict has the attributes so be updates. Attributes names are un camel case, because came from API resources.
        """
        for k, v in patch_dict.iteritems():

            # Attributes into dictionary always camelcase
            if k in schema.declared_fields:
                schema_field = schema.declared_fields[k]
            else:
                raise exception.ValidationError(errors=[{k : "Attribute doesn't exist"}])

            attr_name = schema_field.attribute if schema_field.attribute else schema_field.name
            if isinstance(v, collections.Mapping):

                # Get or create attribute instance
                inner_class = getattr(mapped_class, attr_name).prop.mapper.class_
                inner = getattr(obj, attr_name)
                if not inner:
                    inner = inner_class()

                inner_updated = self._patch(inner, v, schema_field.schema, inner_class)
                setattr(obj, attr_name, inner_updated)

            else:
                if hasattr(schema_field, 'enum') and patch_dict[k]:
                    inner_enum = schema_field.enum
                    setattr(obj, attr_name, inner_enum(patch_dict[k]))
                else:
                    setattr(obj, attr_name, schema_field.deserialize(patch_dict[k]))

        return obj

    def delete(self, object):
        db.session.delete(object)
        db.session.flush()
        return object

    def search(self, filter=None, page=1, per_page=20):
        return self.find_all(filter, page, per_page)

    def find_all(self, filter=None, page=1, per_page=20):
        default_order = desc(self._get_class_field(model.SortCondition('id', 'desc')))
        if not filter:
            items = self.mapped_class.query.order_by(default_order).paginate(page, per_page)
            return model.Pagination(page, per_page, items.total, items.items)
        else:
            if self.schema:
                sql_filters, sql_order = self._create_sql_filter(filter)
                # FIXME : There is an issue when we try to order by more than one creiteria
                sql_order = sql_order if sql_order else default_order
                items = self.mapped_class.query.filter(*sql_filters).order_by(sql_order).paginate(page, per_page)
                return model.Pagination(page, per_page, items.total, items.items)
            else:
                raise exception.ServiceException('This endpoint is not prepared for quering with filters')

    def get_entity_name(self):
        return self. mapped_class.__name__

    def _get_class_field(self, operand):
            """
            This method retrieves the Class Field for quering the database.
            It converts to class field name from the camel case input from the filter
            :param operand:
            :return:
            """
            if self.schema.declared_fields.get(operand.var) is None:
                raise exception.ValidationError('The field {} does not exist as query field'.format(operand.var))

            field = self.schema.declared_fields.get(operand.var).attribute \
                if self.schema.declared_fields.get(operand.var).attribute is not None \
                else self.schema.declared_fields.get(operand.var).name
            if field:
                return self.mapped_class.__dict__.get(field)
            else:
                raise exception.ValidationError('The field {} does not exist as queriable field'.format(operand.var))

    def _create_sql_filter(self, filter):
        """
        Create a SQL filter from uBiome search filter like
        {
          "filter" : {
            "$and" : [
                {"insuranceId" : "6da1a6a7-996c-405a-a6bb-418096978144"},
                {"billed" : "false"},
                {"createdAt": {
                        "$gt" :"2016-12-06"
                    }
                }
            ]
          },
          "order": {
                "createdAt": "desc"
          }
        }
        :param filter:
        :param page:
        :param per_page:
        :return:
        """

        valid_logics = {"$and": "and_", "$or": "or_"}

        filter_sql = []
        for filter_logical in filter.filters:
            filter_logical_or = []
            for operand in filter_logical.operands:
                operator = sql_operator_factory.get_operators(operand.op)
                if filter_logical.op == "$or":
                    filter_logical_or.append(getattr(self._get_class_field(operand), operator)(operand.value))
                else:
                    filter_sql.append(getattr(self._get_class_field(operand), operator)(operand.value))
            if len(filter_logical_or) > 0:
                filter_sql.append(or_(*filter_logical_or))

        filter_order_list = [desc(self._get_class_field(sort)) if sort.order == 'desc' else asc(self._get_class_field(sort)) for sort in filter.sort if filter.sort]

        return filter_sql, filter_order_list

    @contextmanager
    def session_scope(self, rollback=False):
        """Provide a transactional scope around a series of operations."""
        session = db.session
        try:
            yield session
            session.commit() if not rollback and session.is_active else session.rollback()
        except:
            session.rollback()
            raise
        finally:
            session.close()

class SQLAlchemyOperatorFactory:
    """
    This class transforms from mongo type filters to sql alchemy filters operators
    """

    def __init__(self):
        self.valid_ops = {"$eq": '__eq__',
                          "$not": '__ne__',
                          "$in": "in_",
                          "$not_in": "notin_",
                          "$gt": "__gt__",
                          "$lt": "__lt__",
                          "$gte": "__ge__",
                          "$lte": "__le__"}

    def get_operators(self, operand):
        sql_operand = self.valid_ops.get(operand)
        if sql_operand:
            return sql_operand
        else:
            raise exception.ValidationError('operand {} is not valid'.format(operand))

sql_operator_factory = SQLAlchemyOperatorFactory()

class UBiomeServiceDAO():

    def __init__(self, base_url, resource, schema,  version="v1", api_key=None):
        self.base_url = "%s/api/%s/%s" % (base_url,  version , resource)
        self.search_url = "%s/api/%s/search/%s?pageSize={}&pageNumber={}" % (base_url, version, resource)
        self.api_key = api_key if api_key else service.config.get('SECRET_SHARED_KEY')
        self.schema = schema

    def _update_headers(self, headers):

        if not headers:
            headers = {}

        headers.update(
            {service.config.get('UBIOME_AUTH_HEADER'): flask.g.user.jwt if flask.g.get('user') and flask.g.get(
                'user').jwt else self.api_key,
             service.config.get('UBIOME_REQUEST_HEADER'): flask.g.request_id if flask.g.get('request_id') else None})

        return headers

    def retrieve(self, id, headers=None):

        headers = self._update_headers(headers)

        response = requests.get(self.base_url + '/' + str(id), headers=headers if headers else {}, verify=False)

        if response.status_code == 200:
            json_entity = json.loads(response.content)
        else:
            raise exception.ServiceException("Error retreiving entity {} from {} ({})".format(id, self.base_url, response.content))

        entity, errors = self.schema.load(json_entity)
        if errors:
            raise exception.ValidationError(errors=errors)

        return entity

    def find_all(self, filter_dict=None, page=1, per_page=20, headers=None):
        # TODO - Revceive a filter as all DAOs and serialize it

        headers = self._update_headers(headers)

        response = requests.post(self.search_url.format(per_page, page), json=filter_dict,
                                 headers=headers if headers else {}, verify=False)

        if response.status_code == 200:
            json_result = json.loads(response.content)
        else:
            raise exception.ServiceException("Error finding using %s (%s)" % (self.base_url, response.content))

        # Deserialize paginated result
        items, errors = self.schema.load(json_result['items'], many=True)
        if errors:
           raise exception.InvalidDataException("", items, errors)

        page, errors = schema.pagination_schema.load(json_result['page'])
        page['items'] = items

        return page

    def create(self, data, headers=None):

        headers = self._update_headers(headers)

        response = requests.post(self.base_url, json=self.schema.dump(data).data, headers=headers, verify=False)

        if response.status_code == 201:
            json_entity = json.loads(response.content)
        else:
            raise exception.ServiceException(
                "Error creating entity {} from {} ({})".format(id, self.base_url, response.content))

        entity, errors = self.schema.load(json_entity)
        if errors:
            raise exception.ValidationError(errors=errors)

        return entity

    def update(self, id, **kwargs):
        headers = self._update_headers(kwargs.get("headers") if 'headers' in kwargs else {})
        url = "{}/{}"
        response = requests.put(url.format(self.base_url, id), json=kwargs.get("data", {}), headers=headers,
                                verify=False)

        if response.status_code == 200:
            json_entity = json.loads(response.content)
        else:
            raise exception.ServiceException(
                "Error updating entity {} from {} ({})".format(id, self.base_url, response.content))

        entity, errors = self.schema.load(json_entity)
        if errors:
            raise exception.ValidationError(errors=errors)

        return entity