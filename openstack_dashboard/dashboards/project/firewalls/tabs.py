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

from .tables import RulesTable, PoliciesTable, FirewallsTable


class RulesTab(tabs.TableTab):
    table_classes = (RulesTable,)
    name = _("Rules")
    slug = "rules"
    template_name = "horizon/common/_detail_table.html"

    def get_rulestable_data(self):
        try:
            rules = api.fwaas.firewall_rules_get(self.tab_group.request)
            rulesFormatted = [r.readable(self.tab_group.request) for
                              r in rules]
        except:
            rulesFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve rules list.'))
        return rulesFormatted


class PoliciesTab(tabs.TableTab):
    table_classes = (PoliciesTable,)
    name = _("Policies")
    slug = "policies"
    template_name = "horizon/common/_detail_table.html"

    def get_policiestable_data(self):
        try:
            policies = api.fwaas.firewall_policies_get(self.tab_group.request)
            policiesFormatted = [p.readable(self.tab_group.request) for
                              p in policies]
        except:
            policiesFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve policies list.'))
        return policiesFormatted


class FirewallTabs(tabs.TabGroup):
    slug = "fwtabs"
    tabs = (PoliciesTab, RulesTab)
    sticky = True


class RuleDetailsTab(tabs.Tab):
    name = _("Rule Details")
    slug = "ruledetails"
    template_name = "project/firewalls/_rule_details.html"

    def get_context_data(self, request):
        fid = self.tab_group.kwargs['rule_id']
        try:
            rule = api.fwaas.firewall_rule_get(request, fid)
        except:
            rule = []
            exceptions.handle(request,
                              _('Unable to retrieve policy details.'))
        return {'rule': rule}


class PolicyDetailsTab(tabs.Tab):
    name = _("Policy Details")
    slug = "policydetails"
    template_name = "project/firewalls/_policy_details.html"

    def get_context_data(self, request):
        fid = self.tab_group.kwargs['policy_id']
        try:
            policy = api.fwaas.firewall_policy_get(request, fid)
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


class RuleDetailsTabs(tabs.TabGroup):
    slug = "ruletabs"
    tabs = (RuleDetailsTab,)


class PolicyDetailsTabs(tabs.TabGroup):
    slug = "policytabs"
    tabs = (PolicyDetailsTab,)


class FirewallDetailsTabs(tabs.TabGroup):
    slug = "firewalltabs"
    tabs = (FirewallDetailsTab,)
