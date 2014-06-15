from django.conf.urls import patterns, include, url
from tastypie.api import Api

from backgridtest.call_record_resource import CallRecordResource, CallRecordPreference

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

apis = Api(api_name = 'v1')

apis.register(CallRecordResource())
apis.register(CallRecordPreference())

urlpatterns = [url(r'^api/', include(apis.urls)),
               url(r'^testcdrgrid/', 'backgridtest.views.renderTestGrid'),
               url(r'^savepref/', 'backgridtest.views.renderConfigPage'), ]