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


class AddFirewallAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Name"))
    description = forms.CharField(max_length=80, label=_("Description"), required=False)
    firewall_policy_id = forms.ChoiceField(label=_("Policy"))
    admin_state_up = forms.BooleanField(label=_("Admin State"),
                                        initial=True, required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddFirewallAction, self).__init__(request, *args, **kwargs)

        policy_id_choices = [('', _("Select a Policy"))]
        try:
            policies = api.fwaas.firewall_policies_get(request)
        except:
            exceptions.handle(request,
                              _('Unable to retrieve policies list.'))
            policies = []
        for p in policies:
            policy_id_choices.append((p.id, p.name))
        self.fields['firewall_policy_id'].choices = policy_id_choices

    class Meta:
        name = _("AddFirewall")
        permissions = ('openstack.services.network',)
        help_text = _("Create a firewall based on this policy. ")

class AddFirewallStep(workflows.Step):
    action_class = AddFirewallAction
    contributes = ("name", "description", "firewall_policy_id", "admin_state_up")

    def contribute(self, data, context):
        context = super(AddFirewallStep, self).contribute(data, context)
        return context


class AddFirewall(workflows.Workflow):
    slug = "addfirewall"
    name = _("Add Firewall")
    finalize_button_name = _("Add")
    success_message = _('Added Firewall "%s".')
    failure_message = _('Unable to add Firewall "%s".')
    success_url = "horizon:project:firewalls:index"
    default_steps = (AddFirewallStep,)

    def format_status_message(self, message):
        name = self.context.get('name')
        return message % name

    def handle(self, request, context):
        try:
            firewall = api.fwaas.firewall_create(request, **context)
            return True
        except:
            msg = self.format_status_message(self.failure_message)
            exceptions.handle(request, msg)
            return False
