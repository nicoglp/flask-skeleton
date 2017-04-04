import flask
from app.brac import require_auth
from app.base import resource
from app.base.schema import pagination_schema
from app.base import model

class PHIEntityResource(resource.EntityResource):
    """
    Support to basic REST operations over specific entity.
    """

    def __init__(self, dao, schema, validators=None):
        resource.EntityResource.__init__(self, dao, schema, validators)

    @require_auth
    def get(self, id, **kwargs):
        return resource.EntityResource.get(self, id, **kwargs)

    @require_auth
    def post(self, id, **kwargs):
        return resource.EntityResource.post(self, id, **kwargs)

    @require_auth
    def put(self, id, **kwargs):
        return resource.EntityResource.put(self, id, **kwargs)

    @require_auth
    def delete(self, id, **kwargs):
        return resource.EntityResource.delete(self, id, **kwargs)

    @require_auth
    def patch(self, id, **kwargs):
        return resource.EntityResource.patch(self, id, **kwargs)


class PHICollectionResource(resource.CollectionResource):
    """
    Support to basic REST operations over entity's collections.
    """
    @require_auth
    def get(self, **kwargs):

        self._audit_before()

        per_page = flask.request.args.get('pageSize', 20, type=int)
        page = flask.request.args.get('pageNumber', 1, type=int)

        find = model.Find()
        logic = model.FilterLogical('$and')
        logic.operands.append(model.FilterComparator('userId',  '$eq', flask.g.user.id))
        find.filters.append(logic)
        find.sort.append(model.SortCondition('createdAt', 'desc'))

        pagination = self.dao.find_all(find, page=page, per_page=per_page)

        pages, page_errors = pagination_schema.dump(pagination)
        data, data_errors = self.schema.dump(pagination.items, many=True)
        return self._response(dict(items=data,page=pages), 200)

    @require_auth
    def post(self, **kwargs):
        return resource.CollectionResource.post(self, **kwargs)

    @require_auth
    def put(self, **kwargs):
        return resource.CollectionResource.put(self, **kwargs)

    @require_auth
    def patch(self, id, **kwargs):
        return resource.CollectionResource.patch(self, **kwargs)

    @require_auth
    def delete(self, **kwargs):
        return resource.CollectionResource.delete(self, **kwargs)


class PHISearchResource(resource.SearchResource):
    """
    Support search operation over entity's collections.
    """

    def __init__(self, dao, schema):
        resource.SearchResource.__init__(self, dao, schema)

    @require_auth
    def post(self):
        return super(PHISearchResource, self).post()
