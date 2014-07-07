from bson import ObjectId

from tastypie.bundle import Bundle
from tastypie.resources import Resource
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict


class MongoDocument(dict):
    __getattr__ = dict.get

class MongoDBResource(Resource):
    """
    A base resource that allows to make CRUD operations for mongodb.
    """

    def get_object_class(self):
        return self._meta.object_class

    def get_collection(self):
        """
        Encapsulates collection name.
        """
        raise NotImplementedError("You should implement get_collection method.")

    def apply_filters(self, request, applicable_filters):
        if 'sort_by' in applicable_filters:
            sort_key = applicable_filters['sort_by']
            order_by = int(applicable_filters['order_by']) 
            return list(map(self.get_object_class(), self.get_collection().\
                find({"$query":{},"$orderby":{sort_key:order_by}})))
        
        return list(map(self.get_object_class(), self.get_collection().find() ))

    def build_filters(self, filters):
        if isinstance(filters, QueryDict):
            return filters.dict()

        return filters

    def obj_get_list(self, bundle, **kwargs):

        filters = {}
        result = []
        request = bundle.request

        if hasattr(request, 'GET'):
            filters = request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)
        applicable_filters = self.build_filters(filters=filters)

        return self.apply_filters(request, applicable_filters)

    def obj_get(self, bundle, **kwargs):
        """
        Returns mongodb document from provided id.
        """

        obj = self.get_collection().find_one({
            "_id": int(kwargs.get("pk"))
        })

        if not obj:
            raise ObjectDoesNotExist

        self.authorized_read_detail(obj, bundle)

        return self.get_object_class()(obj)