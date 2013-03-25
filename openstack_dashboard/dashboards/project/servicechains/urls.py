# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright 2013, Big Switch Networks, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf.urls.defaults import url, patterns

from .views import IndexView
from .views import AddTemplateView, AddChainView
from .views import TemplateDetailsView, ChainDetailsView

urlpatterns = patterns(
    'openstack_dashboard.dashboards.project.servicechains.views',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^addtemplate$', AddTemplateView.as_view(), name='addtemplate'),
    url(r'^addchain/(?P<template_id>[^/]+)/$', AddChainView.as_view(), name='addchain'),
    url(r'^template/(?P<template_id>[^/]+)/$',
        TemplateDetailsView.as_view(), name='templatedetails'),
    url(r'^chain/(?P<chain_id>[^/]+)/$',
        ChainDetailsView.as_view(), name='chaindetails'))
