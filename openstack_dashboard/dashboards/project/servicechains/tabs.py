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

from .tables import TemplatesTable, ChainsTable

class Template():
    id = 'id'
    name = 'name'

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Chain():
    id = 'id'
    name = 'name'

    def __init__(self, id, name):
        self.id = id
        self.name = name

class TemplatesTab(tabs.TableTab):
    table_classes = (TemplatesTable,)
    name = _("Templates")
    slug = "templates"
    template_name = "horizon/common/_detail_table.html"

    def get_templatestable_data(self):
        try:
            templates = api.scaas.templates_get(self.tab_group.request)
            templatesFormatted = [p.readable(self.tab_group.request) for
                              p in templates]
        except:
            templatesFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve policies list.'))
        templatesFormatted.append(Template('myid', 'myname'))
        return templatesFormatted


class ChainsTab(tabs.TableTab):
    table_classes = (ChainsTable,)
    name = _("Chains")
    slug = "chains"
    template_name = "horizon/common/_detail_table.html"

    def get_chainstable_data(self):
        try:
            chains = api.scaas.chains_get(self.tab_group.request)
            chainsFormatted = [c.readable(self.tab_group.request) for
                                c in chains]
        except:
            chainsFormatted = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve service chains list.'))
        chainsFormatted.append(Chain('myid', 'myname'))
        return chainsFormatted


class ChainTabs(tabs.TabGroup):
    slug = "sctabs"
    tabs = (TemplatesTab, ChainsTab)
    sticky = True


class TemplateDetailsTab(tabs.Tab):
    name = _("Template Details")
    slug = "templatedetails"
    template_name = "project/servicechains/_template_details.html"

    def get_context_data(self, request):
        tid = self.tab_group.kwargs['template_id']
        try:
            template = api.scaas.template_get(request, tid)
        except:
            template = []
            exceptions.handle(request,
                              _('Unable to retrieve template details.'))
        return {'template': template}


class ChainDetailsTab(tabs.Tab):
    name = _("Service Chain Details")
    slug = "chaindetails"
    template_name = "project/servicechains/_chain_details.html"

    def get_context_data(self, request):
        sid = self.tab_group.kwargs['chain_id']
        try:
            chain = api.scaas.chain_get(request, sid)
        except:
            chain = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve service chain details.'))
        return {'chain': chain}


class TemplateDetailsTabs(tabs.TabGroup):
    slug = "templatetabs"
    tabs = (TemplateDetailsTab,)


class ChainDetailsTabs(tabs.TabGroup):
    slug = "chaintabs"
    tabs = (ChainDetailsTab,)
