import json
from ast import literal_eval

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.paginator import Paginator
from tastypie.authorization import Authorization

from backgridtest.models import callrecord, callrecordpreference

class CallRecordResource(ModelResource):
    
    class Meta:
        queryset = callrecord.objects.filter(user_plan_id=1684)
        resource_name = 'callrecords'
        allowed_methods = ['get']
        paginator_class = Paginator
        ordering = ['start_time', 'billed_pulses', 'coins_deducted', 'duration']

    def alter_list_data_to_serialize(self, request, data):
        callrecord_pref = callrecordpreference.objects.get(pk=2)
        data['pref'] = callrecord_pref.preference
        return data

class CallRecordPreference(ModelResource):

    class Meta:
        queryset = callrecordpreference.objects.all()
        resource_name = 'callrecordpref'
        allowed_methods = ['get', 'post', 'put']
        authorization= Authorization()

    def alter_list_data_to_serialize(self, request, data):
        bundle = data['objects'][0]
        bundle.data['preference'] = literal_eval(bundle.data['preference'])
        data['objects'][0] = bundle
        return data

    '''def dehydrate(self, bundle):
        pref_dict = {}
        print json.loads(bundle.data['preference'].encode('utf-8')))
        for k,v in bundle.data['preference'].encode('utf-8'):
            pref_dict[k.encode('utf-8')] = v

        bundle.data['preference'] = pref_dict    
        return bundle'''