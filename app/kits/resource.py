from app import api
from app.base import resource as base
from app.phi import resource as phi
import schema, dao


api.add_resource(phi.PHIEntityResource,
                 '/kits/<string:id>',
                 resource_class_args=(dao.kit_dao, schema.kit_schema),
                 endpoint='Kit::Entity')

api.add_resource(phi.PHICollectionResource,
                 '/kits',
                 resource_class_args=(dao.kit_dao, schema.kit_schema),
                 endpoint='Kit::Collection')

api.add_resource(phi.PHISearchResource,
                 '/search/kits',
                 resource_class_args=(dao.kit_dao, schema.kit_schema),
                 endpoint='Kit::Search')

api.add_resource(base.EntityResource,
                 '/kit-types/<string:id>',
                 resource_class_args=(dao.kit_type_dao, schema.kit_type_schema),
                 endpoint='KitType::Entity')

api.add_resource(base.CollectionResource,
                 '/kit-types',
                 resource_class_args=(dao.kit_type_dao, schema.kit_type_schema),
                 endpoint='KitType::Collection')

api.add_resource(base.SearchResource,
                 '/search/kit-types',
                 resource_class_args=(dao.kit_type_dao, schema.kit_type_schema),
                 endpoint='KitType::Search')