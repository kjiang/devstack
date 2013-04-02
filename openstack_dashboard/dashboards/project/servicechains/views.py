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

from .workflows import AddServiceChain
from .tabs import ServiceChainTabs, ServiceChain
from .tabs import ServiceChainTemplateDetailsTabs, ServiceChainDetailsTabs
from .tables import ServiceChainsTable

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    table_class = ServiceChainsTable
    template_name = 'project/servicechains/index.html'

    def get_data(self):
        try:
            scs = api.scaas.service_chains_get(self.request)
            scsFormatted = [s.readable(self.request) for
                            s in scs]
        except:
            scsFormatted = []
            exceptions.handle(self.request,
                              _('Unable to retrieve service chain list.'))
        scsFormatted.append(ServiceChain('myid','myname'))
        return scsFormatted


class ManageResourcesView(tabs.TabView):
    tab_group_class = (ServiceChainTabs)
    template_name = 'project/servicechains/details_tabs.html'


class AddServiceChainView(workflows.WorkflowView):
    workflow_class = AddServiceChain
    template_name = "project/servicechains/addchain.html"

    def get_context_data(self, **kwargs):
        context = super(AddServiceChainView, self).get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super(AddServiceChainView, self).get_initial()
        return initial


class ServiceChainTemplateDetailsView(tabs.TabView):
    tab_group_class = (ServiceChainTemplateDetailsTabs)
    template_name = 'project/servicechains/details_tabs.html'


class ServiceChainDetailsView(tabs.TabView):
    tab_group_class = (ServiceChainDetailsTabs)
    template_name = 'project/servicechains/details_tabs.html'
