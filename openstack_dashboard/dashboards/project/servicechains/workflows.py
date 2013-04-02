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


class AddServiceChainAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Name"))
    description = forms.CharField(max_length=80, label=_("Description"), required=False, initial='')
    service_chain_template_id = forms.ChoiceField(label=_("Service Chain Template"))
    source_network = forms.CharField(max_length=80, label=_("Source Network"))
    destination_network = forms.CharField(max_length=80, label=_("Destination Network"))
    services_list = forms.MultipleChoiceField(label=_("Service(s)"),
                                              required=False,
                                              initial=["default"],
                                              widget=forms.CheckboxSelectMultiple(),
                                              help_text=_("Select services for this chain."))
    admin_state_up = forms.BooleanField(label=_("Admin State"),
                                        initial=True, required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddServiceChainAction, self).__init__(request, *args, **kwargs)

        template_id_choices = [('', _("Select a Template"))]
        try:
            templates = api.scaas.service_chain_templates_get(request)
        except:
            exceptions.handle(request,
                              _('Unable to retrieve service chain templates list.'))
            templates = []
        for t in templates:
            template_id_choices.append((t.id, t.name))
        template_id_choices.append(('e5cb1e5f-c41f-4c85-a787-206f9afb16be', 'template 1'))
        template_id_choices.append(('e5cb1e5f-c41f-4c85-a787-206f9afb16ce', 'template 2'))
        self.fields['service_chain_template_id'].choices = template_id_choices

    class Meta:
        name = _("AddServiceChain")
        permissions = ('openstack.services.network',)
        help_text = _("Create a service chain based on this template. ")


class AddServiceChainStep(workflows.Step):
    action_class = AddServiceChainAction
    contributes = ("name", "description", "service_chain_template_id", "source_network", "destination_network", "services_list")

    def contribute(self, data, context):
        context = super(AddServiceChainStep, self).contribute(data, context)
        return context


class AddServiceChain(workflows.Workflow):
    slug = "addchain"
    name = _("Add Service Chain")
    finalize_button_name = _("Add")
    success_message = _('Added Service Chain "%s".')
    failure_message = _('Unable to add Service Chain "%s".')
    success_url = "horizon:project:servicechains:index"
    default_steps = (AddServiceChainStep,)

    def format_status_message(self, message):
        name = self.context.get('name')
        return message % name

    def handle(self, request, context):
        try:
            chain = api.scaas.service_chain_create(request, **context)
            return True
        except:
            msg = self.format_status_message(self.failure_message)
            exceptions.handle(request, msg)
            return False
