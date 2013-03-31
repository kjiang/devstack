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

import re

from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import tabs
from horizon import tables

from openstack_dashboard import api

from .tables import PoliciesTable, FirewallsTable

class Policy():
    id = 'id'
    name = 'name'

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Firewall():
    id = 'id'
    name = 'name'

    def __init__(self, id, name):
        self.id = id
        self.name = name

class PoliciesTab(tabs.TableTab):
    table_classes = (PoliciesTable,)
    name = _("Policies")
    slug = "policies"
    template_name = "horizon/common/_detail_table.html"

    def get_policiestable_data(self):
        try:
            policies = api.fwaas.policies_get(self.tab_group.request)
            policiesFormatted = [p.readable(self.tab_group.request) for
                              p in policies]
        except:
            policiesFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve policies list.'))
        policiesFormatted.append(Policy('myid','myname')) 
        return policiesFormatted


class FirewallsTab(tabs.TableTab):
    table_classes = (FirewallsTable,)
    name = _("Firewalls")
    slug = "firewalls"
    template_name = "horizon/common/_detail_table.html"

    def get_firewallstable_data(self):
        try:
            firewalls = api.fwaas.firewalls_get(self.tab_group.request)
            firewallsFormatted = [f.readable(self.tab_group.request) for
                                f in firewalls]
        except:
            firewallsFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve firewall list.'))
        firewallsFormatted.append(Firewall('myid','myname'))
        return firewallsFormatted


class FirewallTabs(tabs.TabGroup):
    slug = "fwtabs"
    tabs = (FirewallsTab,)
    sticky = True


class PolicyDetailsTab(tabs.Tab):
    name = _("Policy Details")
    slug = "policydetails"
    template_name = "project/firewalls/_policy_details.html"

    def get_context_data(self, request):
        pid = self.tab_group.kwargs['policy_id']
        try:
            policy = api.fwaas.policy_get(request, pid)
        except:
            policy = []
            exceptions.handle(request,
                              _('Unable to retrieve policy details.'))
        return {'policy': policy}


class FirewallDetailsTab(tabs.Tab):
    name = _("Firewall Details")
    slug = "firewalldetails"
    template_name = "project/firewalls/_firewall_details.html"

    def get_context_data(self, request):
        fid = self.tab_group.kwargs['firewall_id']
        try:
            firewall = api.fwaas.firewall_get(request, fid)
        except:
            firewall = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve firewall details.'))
        return {'firewall': firewall}


class PolicyDetailsTabs(tabs.TabGroup):
    slug = "policytabs"
    tabs = (PolicyDetailsTab,)


class FirewallDetailsTabs(tabs.TabGroup):
    slug = "firewalltabs"
    tabs = (FirewallDetailsTab,)
