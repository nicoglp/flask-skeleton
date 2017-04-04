import re
import datetime

from marshmallow import ValidationError, Schema, fields, validate
from marshmallow.fields import String, DateTime
from marshmallow.utils import isoformat



from functools import partial
from . import model
from app.base.exception import ValidationError as FilterError

import re

def __must_not_be_blank(field, data):
    if not data:
        raise ValidationError('Field {} must not be blank.'.format(field))

def not_blank(field_name):
    return partial(__must_not_be_blank, field_name)


def __entity_exist(field, dao, data):
    if data:
        try:
            entity = dao.retrieve(data)
            if not entity:
                raise ValidationError("Entity not found with id {}".format(data))
        except ValidationError as e:
            raise ValidationError("Error retrieving entity with {} ({})".format(data, e.message))

def entity_exist(field_name, dao):
    return partial(__entity_exist, field_name, dao)


def __entity_exist_in_iterable(field, list, data):
    if data:
        if not any([data in list]):
            raise ValidationError("The attribute does not match with any available value '{}'".format(data))


def entity_exist_in_iterable(field_name, list):
    """
    This method checks if an element exist in a list. Also,
    :param field_name:
    :param dao:
    :return:
    """
    return partial(__entity_exist_in_iterable, field_name, list)


def __entity_exist_in_iterable_dict(field, list, attribute, data):
    if data:
        if not True in [data == element[attribute] for element in list]:
            raise ValidationError("The attribute {} does not match with any available value in insurances company list".format(field))


def entity_exist_in_iterable_dict(field, list, attribute):
    """
    This method checks if an element exist in every element from a dictionary inside  a list
    :param field_name:
    :param dao:
    :return:
    """
    return partial(__entity_exist_in_iterable_dict, field, list, attribute)

class UUID(String):

    """A UUID field."""
    default_error_messages = {
        'invalid_uuid': 'Not a valid UUID field.'
    }

    def __init__(self, *args, **kwargs):
        String.__init__(self, *args, **kwargs)
        self.regex = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def _validated(self, value):
        """Format the value or raise a :exc:`ValidationError` if an error occurs."""
        if value is None:
            return None
        return validate.Regexp(self.regex, flags=re.IGNORECASE,
            error=self.error_messages['invalid_uuid']
        )(str(value))

    def _serialize(self, value, attr, obj):
        validated = str(self._validated(value)) if value is not None else None
        return super(String, self)._serialize(validated, attr, obj)

    def _deserialize(self, value, attr, data):
        return self._validated(value)

class BaseSchema(Schema):

    def __init__(self, **kwargs):
        super(BaseSchema, self).__init__( **kwargs)

    id = UUID(allow_none=True, required=False, dump_only=False)

base_schema = BaseSchema()


class PaginationSchema(Schema):

    pageNumber = fields.Integer(attribute='page')
    pageSize = fields.Integer(attribute='per_page')
    totalPages = fields.Integer(attribute='pages')
    totalItems = fields.Integer(attribute='total')
    errors = fields.Integer()

pagination_schema = PaginationSchema()


def parse_filter(find_param):
    filters = []
    default_ords = []

    for key, cond in find_param.iteritems():

        if key.startswith('$'):
            # Logical $and or $or operators.

            if key not in ["$and", "$or"]:
                raise FilterError(errors={key:"Logical operator is not supported"})
            if not isinstance(cond, list):
                raise FilterError(errors={key:"Logical operators must be a list of conditions"})

            filter = model.FilterLogical(key)
            for c in cond:
                # List must contains a list of dictionaries (conditions with operators)
                filter.operands.append(parser_conditions(c))

            filters.append(filter)

        else:
            # Simple operator
            default_ords.append(parser_conditions({key:cond}))

    if len(default_ords) > 0:
        default_and = model.FilterLogical("$and")
        default_and.operands = default_ords
        filters.append(default_and)

    return filters


def parser_conditions(dictionary):
    """
    Conditions could be a single equal condition (just a value) a condition with an operator.
    :return:
    """
    if len(dictionary) != 1:
        raise FilterError(errors={"object" : "Condition allows just one property"})

    var, value = dictionary.items()[0]

    if isinstance(value, dict):
        # 'value' is an operator
        if len(value) > 1:
            raise FilterError(errors={var : "Just one condition is allowed for this attribute ({} was provides)".format(len(value))})

        operator, op_value = value.items()[0]
        if operator not in ['$eq', '$not', '$gt', '$gte', '$lt', '$lte', '$not_in', '$in']:
            raise FilterError(errors={operator : "Operator is not supported"})

        return model.FilterComparator(var, operator, op_value )
    else:
        # 'value' is the equals value
        return model.FilterComparator(var, "$eq", value)


def parse_order(sort_param):

    sorts = []
    for var, order in sort_param.iteritems():
        sorts.append(model.SortCondition(var, order))
    return sorts

class PHI(String):

    """A UUID field."""
    default_error_messages = {
        'invalid_phi': 'Not a valid PHI field.'
    }

    def __init__(self, *args, **kwargs):
        String.__init__(self, *args, **kwargs)
        self.regex = r'{pi:([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})}'

    def _validated(self, value):
        """Format the value or raise a :exc:`ValidationError` if an error occurs."""
        if not value:
            return None
        return validate.Regexp(self.regex, flags=re.IGNORECASE,
            error=self.error_messages['invalid_phi']
        )(value)

    def _serialize(self, value, attr, obj):
        validated = str(self._validated(value)) if value is not None else None
        return super(String, self)._serialize(validated, attr, obj)

    def _deserialize(self, value, attr, data):
        return self._validated(value)

class DateToDatetime(DateTime):

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            return isoformat(datetime.datetime.combine(value, datetime.time.min))
        except AttributeError:
            self.fail('format', input=value)
