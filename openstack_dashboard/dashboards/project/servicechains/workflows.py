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

from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms
from horizon.utils import fields
from horizon import workflows

from openstack_dashboard import api


LOG = logging.getLogger(__name__)


class AddTemplateAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Name"))

    def __init__(self, request, *args, **kwargs):
        super(AddTemplateAction, self).__init__(request, *args, **kwargs)

    class Meta:
        name = _("AddTemplate")
        permissions = ('openstack.services.network',)
        help_text = _("Create Service Chain Template")

class AddTemplateStep(workflows.Step):
    action_class = AddTemplateAction
    contributes = ("name",)

    def contribute(self, data, context):
        context = super(AddTemplateStep, self).contribute(data, context)
        if data:
            return context


class AddTemplate(workflows.Workflow):
    slug = "addtemplate"
    name = _("Add Template")
    finalize_button_name = _("Add")
    success_message = _('Added Template "%s".')
    failure_message = _('Unable to add Template "%s".')
    success_url = "horizon:project:servicechains:index"
    default_steps = (AddTemplateStep,)

    def format_status_message(self, message):
        name = self.context.get('name')
        return message % name

    def handle(self, request, context):
        try:
            template = api.scaas.template_create(request, **context)
            return True
        except:
            msg = self.format_status_message(self.failure_message)
            exceptions.handle(request, msg)
            return False


class AddChainAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Name"))

    def __init__(self, request, *args, **kwargs):
        super(AddChainAction, self).__init__(request, *args, **kwargs)

    class Meta:
        name = _("AddChain")
        permissions = ('openstack.services.network',)
        help_text = _("Create a service chain based on this template. ")


class AddChainStep(workflows.Step):
    action_class = AddChainAction
    contributes = ("name",)

    def contribute(self, data, context):
        context = super(AddChainStep, self).contribute(data, context)
        return context


class AddChain(workflows.Workflow):
    slug = "addchain"
    name = _("Add Service Chain")
    finalize_button_name = _("Add")
    success_message = _('Added Service Chain "%s".')
    failure_message = _('Unable to add Service Chain "%s".')
    success_url = "horizon:project:servicechains:index"
    default_steps = (AddChainStep,)

    def format_status_message(self, message):
        name = self.context.get('name')
        return message % name

    def handle(self, request, context):
        try:
            chain = api.scaas.chain_create(request, **context)
            return True
        except:
            msg = self.format_status_message(self.failure_message)
            exceptions.handle(request, msg)
            return False
