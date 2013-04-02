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

from .tables import LoadBalancersTable, PoolsTable, MembersTable, MonitorsTable


#class Lb():
#    id = 'id'
#    name = 'name'

#    def __init__(self, id, name):
#        self.id = id
#        self.name = name


class LoadBalancersTab(tabs.TableTab):
    table_classes = (LoadBalancersTable,)
    name = _("LoadBalancers")
    slug = "loadbalancers"
    template_name = "horizon/common/_detail_table.html"

    def get_loadbalancerstable_data(self):
        try:
            lbs = api.lbaas.lbs_get(self.tab_group.request)
            lbsFormatted = [l.readable(self.tab_group.request) for
                                l in lbs]
        except:
            lbsFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve loadbalancer list.'))
        lbsFormatted.append(Lb('myid','myname'))
        return lbsFormatted


class PoolsTab(tabs.TableTab):
    table_classes = (PoolsTable,)
    name = _("Pools")
    slug = "pools"
    template_name = "horizon/common/_detail_table.html"

    def get_poolstable_data(self):
        try:
            pools = api.lbaas.pools_get(self.tab_group.request)
            poolsFormatted = [p.readable(self.tab_group.request) for
                              p in pools]
        except:
            poolsFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve pools list.'))
        return poolsFormatted


class MembersTab(tabs.TableTab):
    table_classes = (MembersTable,)
    name = _("Members")
    slug = "members"
    template_name = "horizon/common/_detail_table.html"

    def get_memberstable_data(self):
        try:
            members = api.lbaas.members_get(self.tab_group.request)
            membersFormatted = [m.readable(self.tab_group.request) for
                                m in members]
        except:
            membersFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve member list.'))
        return membersFormatted


class MonitorsTab(tabs.TableTab):
    table_classes = (MonitorsTable,)
    name = _("Monitors")
    slug = "monitors"
    template_name = "horizon/common/_detail_table.html"

    def get_monitorstable_data(self):
        try:
            monitors = api.lbaas.pool_health_monitors_get(
                self.tab_group.request)
        except:
            monitors = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve monitor list.'))
        return monitors


class LoadBalancerTabs(tabs.TabGroup):
    slug = "lbtabs"
    tabs = (PoolsTab, MembersTab, MonitorsTab)
    sticky = True


class LbDetailsTab(tabs.Tab):
    name = _("Load Balancer Details")
    slug = "lbdetails"
    template_name = "project/loadbalancers/_lb_details.html"

    def get_context_data(self, request):
        pid = self.tab_group.kwargs['lb_id']
        try:
            lb = api.lbaas.loadbalancer_get(request, pid)
        except:
            lb = []
            exceptions.handle(request,
                              _('Unable to retrieve load balancer details.'))
        return {'lb': lb}


class PoolDetailsTab(tabs.Tab):
    name = _("Pool Details")
    slug = "pooldetails"
    template_name = "project/loadbalancers/_pool_details.html"

    def get_context_data(self, request):
        pid = self.tab_group.kwargs['pool_id']
        try:
            pool = api.lbaas.pool_get(request, pid)
        except:
            pool = []
            exceptions.handle(request,
                              _('Unable to retrieve pool details.'))
        return {'pool': pool}


class VipDetailsTab(tabs.Tab):
    name = _("Vip Details")
    slug = "vipdetails"
    template_name = "project/loadbalancers/_vip_details.html"

    def get_context_data(self, request):
        vid = self.tab_group.kwargs['vip_id']
        try:
            vip = api.lbaas.vip_get(request, vid)
        except:
            vip = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve vip details.'))
        return {'vip': vip}


class MemberDetailsTab(tabs.Tab):
    name = _("Member Details")
    slug = "memberdetails"
    template_name = "project/loadbalancers/_member_details.html"

    def get_context_data(self, request):
        mid = self.tab_group.kwargs['member_id']
        try:
            member = api.lbaas.member_get(request, mid)
        except:
            member = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve member details.'))
        return {'member': member}


class MonitorDetailsTab(tabs.Tab):
    name = _("Monitor Details")
    slug = "monitordetails"
    template_name = "project/loadbalancers/_monitor_details.html"

    def get_context_data(self, request):
        mid = self.tab_group.kwargs['monitor_id']
        try:
            monitor = api.lbaas.pool_health_monitor_get(request, mid)
        except:
            monitor = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve monitor details.'))
        return {'monitor': monitor}


class LbDetailsTabs(tabs.TabGroup):
    slug = "lbtabs"
    tabs = (LbDetailsTab,)


class PoolDetailsTabs(tabs.TabGroup):
    slug = "pooltabs"
    tabs = (PoolDetailsTab,)


class VipDetailsTabs(tabs.TabGroup):
    slug = "viptabs"
    tabs = (VipDetailsTab,)


class MemberDetailsTabs(tabs.TabGroup):
    slug = "membertabs"
    tabs = (MemberDetailsTab,)


class MonitorDetailsTabs(tabs.TabGroup):
    slug = "monitortabs"
    tabs = (MonitorDetailsTab,)
