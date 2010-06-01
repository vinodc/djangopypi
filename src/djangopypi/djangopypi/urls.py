# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns("djangopypi.views",
    url(r'^$', "root", name="djangopypi-root"),
    url(r'^packages/$','packages.index', name='djangopypi-package-index'),
    url(r'^search/$','packages.search',name='djangopypi-search'),
    url(r'^pypi/$', 'releases.index', name='djangopypi-release-index'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/$','packages.details',
        name='djangopypi-package'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<release>[\w\d_\.\-]+)/$',
        'releases.details',name='djangopypi-release'),
    
    
    
)