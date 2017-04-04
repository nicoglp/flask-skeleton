from math import ceil
from datetime import datetime

from sqlalchemy import Column, types
from sqlalchemy.orm import class_mapper
from app import db

DEFAULT_WITH_DELETE_CASCADE = 'save-update, merge, delete, delete-orphan, expunge'


class BaseModel(object):

    id = None

    def __init__(self, *initial_data, **kwargs):
        """
        Allows instantiate an object with a dictionary or a list of params
        as argument of the constructor method.
        """
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class BaseDBModel(BaseModel, db.Model):

    __abstract__ = True

    id = Column(types.String(36), server_default="gen_random_uuid()", primary_key=True)

    def _to_dict(self, obj, found=None):
        """
        Generates a ``dict()`` representation of the persistent object, with just the mapped attributes.
        For a more complex serialization use '''marshallmallow.Schema'''
        """
        if found is None:
            found = set()
        mapper = class_mapper(obj.__class__)
        columns = [column.key for column in mapper.columns]
        get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (c, getattr(obj, c))
        out = dict(map(get_key_value, columns))
        for name, relation in mapper.relationships.items():
            if relation not in found:
                found.add(relation)
                related_obj = getattr(obj, name)
                if related_obj is not None:
                    if relation.uselist:
                        out[name] = [self._to_dict(child, found) for child in related_obj]
                    else:
                        out[name] = self._to_dict(related_obj, found)
        return out


class Pagination(object):

    def __init__(self, page, per_page, total, items, invalid_data=None):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items
        self.invalid_data = invalid_data if invalid_data else []

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        return self.page + 1

    @property
    def errors(self):
        return len(self.invalid_data)

class Find(BaseModel):

    def __init__(self):
        super(Find, self).__init__()
        self.filters = []
        self.sort = []

    def is_empty(self):
        return not bool(self.filters or self.sort)


class FilterOperator(BaseModel):

    def __init__(self, operator):
        super(FilterOperator, self).__init__()
        self.op = operator

class FilterLogical(FilterOperator):

    def __init__(self, op):
        super(FilterLogical, self).__init__(op)
        self.operands = []

class FilterComparator(FilterOperator):
    def __init__(self, var, op, value):
        super(FilterComparator, self).__init__(op)
        self.var = var
        self.value = value

class SortCondition(BaseModel):

    def __init__(self, var, order):
        super(SortCondition, self).__init__()
        self.var = var
        self.order = order