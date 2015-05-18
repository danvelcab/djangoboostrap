from django.conf.urls import url, patterns
from twitterpromo.views.all.IndexAllView import IndexAllView

__author__ = 'Daniel'

urlpatterns = patterns('',
                       url(r'^$', IndexAllView.index, name = 'index'),
                       )
