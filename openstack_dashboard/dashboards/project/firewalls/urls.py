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
from .views import AddFirewallView
from .views import PolicyDetailsView, FirewallDetailsView, ManageFirewallView

urlpatterns = patterns(
    'openstack_dashboard.dashboards.project.firewalls.views',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^managefirewall$', ManageFirewallView.as_view(), name='managefirewall'),
    url(r'^addfirewall$', AddFirewallView.as_view(), name='addfirewall'),
    url(r'^policy/(?P<policy_id>[^/]+)/$',
        PolicyDetailsView.as_view(), name='policydetails'),
    url(r'^firewall/(?P<firewall_id>[^/]+)/$',
        FirewallDetailsView.as_view(), name='firewalldetails'))
