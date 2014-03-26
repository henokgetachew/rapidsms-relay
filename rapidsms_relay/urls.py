from django.conf.urls import patterns, url

from rapidsms_relay import views

urlpatterns = patterns('',
    url(r'^$',views.index, name = 'index')
                       
)