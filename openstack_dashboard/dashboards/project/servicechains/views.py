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

from .workflows import AddTemplate, AddChain
from .tabs import ChainTabs
from .tabs import TemplateDetailsTabs, ChainDetailsTabs


LOG = logging.getLogger(__name__)


class IndexView(tabs.TabView):
    tab_group_class = (ChainTabs)
    template_name = 'project/servicechains/details_tabs.html'

    def post(self, request, *args, **kwargs):
        obj_ids = request.POST.getlist('object_ids')
        action = request.POST['action']
        m = re.search('.delete([a-z]+)', action).group(1)
        if obj_ids == []:
            obj_ids.append(re.search('([0-9a-z-]+)$', action).group(1))
        if m == 'template':
            for obj_id in obj_ids:
                try:
                    api.scaas.template_delete(request, obj_id)
                except:
                    exceptions.handle(request,
                                      _('Unable to delete template.'))
        if m == 'chain':
            for obj_id in obj_ids:
                try:
                    api.scaas.chain_delete(request, obj_id)
                except:
                    exceptions.handle(request,
                                      _('Unable to delete chain.'))
        return self.get(request, *args, **kwargs)


class AddTemplateView(workflows.WorkflowView):
    workflow_class = AddTemplate
    template_name = "project/servicechains/addtemplate.html"

    def get_initial(self):
        initial = super(AddTemplateView, self).get_initial()
        return initial


class AddChainView(workflows.WorkflowView):
    workflow_class = AddChain
    template_name = "project/servicechains/addchain.html"

    def get_context_data(self, **kwargs):
        context = super(AddChainView, self).get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super(AddChainView, self).get_initial()
        initial['template_id'] = self.kwargs['template_id']
        try:
            template = api.scaas.template_get(self.request, initial['template_id'])
        except:
            msg = _('Unable to retrieve template.')
            exceptions.handle(self.request, msg)
        return initial


class TemplateDetailsView(tabs.TabView):
    tab_group_class = (TemplateDetailsTabs)
    template_name = 'project/servicechains/details_tabs.html'


class ChainDetailsView(tabs.TabView):
    tab_group_class = (ChainDetailsTabs)
    template_name = 'project/servicechains/details_tabs.html'
