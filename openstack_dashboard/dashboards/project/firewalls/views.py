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

import logging
import re

from django import http
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import tables
from horizon import tabs
from horizon import workflows

from openstack_dashboard import api

from .workflows import AddPolicy, AddFirewall
from .tabs import Firewall, FirewallTabs
from .tabs import PolicyDetailsTabs, FirewallDetailsTabs
from .tables import FirewallsTable

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    table_class = FirewallsTable
    template_name = 'project/firewalls/index.html'

    def get_data(self):
        try:
            fws = api.fwaas.firewalls_get(self.request)
            fwsFormatted = [f.readable(self.request) for
                                f in fws]
        except:
            fwsFormatted = []
            exceptions.handle(self.request,
                              _('Unable to retrieve firewall list.'))
        fwsFormatted.append(Firewall('myid','myname', 'description', 'direction', 'firewall_policy_id'))
        return fwsFormatted


class ManageFirewallView(tabs.TabView):
    tab_group_class = (FirewallTabs)
    template_name = 'project/firewalls/details_tabs.html'


class AddPolicyView(workflows.WorkflowView):
    workflow_class = AddPolicy
    template_name = "project/firewalls/addpolicy.html"

    def get_initial(self):
        initial = super(AddPolicyView, self).get_initial()
        return initial


class AddFirewallView(workflows.WorkflowView):
    workflow_class = AddFirewall
    template_name = "project/firewalls/addfirewall.html"

    def get_context_data(self, **kwargs):
        context = super(AddFirewallView, self).get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super(AddFirewallView, self).get_initial()
        return initial


class PolicyDetailsView(tabs.TabView):
    tab_group_class = (PolicyDetailsTabs)
    template_name = 'project/firewalls/details_tabs.html'


class FirewallDetailsView(tabs.TabView):
    tab_group_class = (FirewallDetailsTabs)
    template_name = 'project/firewalls/details_tabs.html'
