import json
from ast import literal_eval

from django.conf import settings
from tastypie import fields
from tastypie.paginator import Paginator
from tastypie.authorization import Authorization

#from tastypie_mongodb.resources import MongoDBResource
from backgridtest.mongo_resource import MongoDocument, MongoDBResource


db = settings.MONGO_DB_CONN

class CallRecordResource(MongoDBResource):
    
    _id = fields.IntegerField(attribute="_id")
    start_time = fields.DateTimeField(attribute="start_time")
    billed_pulses = fields.IntegerField(attribute="billed_pulses")
    callerph = fields.CharField(attribute="callerph")
    extension = fields.IntegerField(attribute="extension", null=True)
    filepath = fields.CharField(attribute="filepath")
    callid = fields.CharField(attribute="callid")
    ftype = fields.CharField(attribute="ftype")
    sr_number = fields.CharField(attribute="sr_number")
    duration = fields.IntegerField(attribute="duration")
    voiceid = fields.CharField(attribute="voiceid")
    coins_deducted = fields.IntegerField(attribute="coins_deducted")

    class Meta:
        resource_name = 'callrecords'
        allowed_methods = ['get']
        ordering = ['start_time', 'billed_pulses', 'coins_deducted', 'duration']
        collection = "call_records"
        object_class = MongoDocument

    def get_collection(self):
       return db[self._meta.collection]

    def alter_list_data_to_serialize(self, request, data):
        callrecord_pref = db.call_record_pref.find({"_id":1})
        call_rec = callrecord_pref.next()
        data['pref'] = call_rec["preference"]
        data['order_pref'] = call_rec["order_preference"]
        return data

class CallRecordPreference(MongoDBResource):

    _id = fields.IntegerField(attribute="_id")
    preference = fields.CharField(attribute="preference")
    order_preference = fields.CharField(attribute="order_preference")

    class Meta:

        resource_name = 'callrecordpref'
        allowed_methods = ['get', 'post', 'put']
        authorization= Authorization()
        object_class = MongoDocument
        collection = "call_record_pref"

    def get_collection(self):
        return db[self._meta.collection]

    def dehydrate(self, bundle):
        bundle.data['preference'] = literal_eval(bundle.data['preference'])
        bundle.data['order_preference'] = literal_eval(bundle.data['order_preference'])
        return bundle

    def obj_update(self, bundle, **kwargs):
        """
        Updates mongodb document.
        """
        print bundle.data
        self.authorized_update_detail(bundle.data, bundle)
        self.get_collection().update(
            {"_id": int(kwargs.get("pk"))},
            {"$set": bundle.data}
        )

        return bundle