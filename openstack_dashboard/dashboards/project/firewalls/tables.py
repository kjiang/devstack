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

from django.utils import http
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from horizon import tables
from openstack_dashboard import api


LOG = logging.getLogger(__name__)


class AddPolicyLink(tables.LinkAction):
    name = "addpolicy"
    verbose_name = _("Add Policy")
    url = "horizon:project:firewalls:addpolicy"
    classes = ("btn-addpolicy",)


class AddFirewallLink(tables.LinkAction):
    name = "addfirewall"
    verbose_name = _("Create Firewall from Policy")
    classes = ("btn-addfirewall",)

    def get_link_url(self, policy):
        base_url = reverse("horizon:project:firewalls:addfirewall",
                           kwargs={'policy_id': policy.id})
        return base_url


class DeletePolicyLink(tables.DeleteAction):
    name = "deletepolicy"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Policy")
    data_type_plural = _("Policies")


class DeleteFirewallLink(tables.DeleteAction):
    name = "deletefirewall"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Firewall")
    data_type_plural = _("Firewalls")


class PoliciesTable(tables.DataTable):
    name = tables.Column("name",
                       verbose_name=_("Name"))
    class Meta:
        name = "policiestable"
        verbose_name = _("Policies")
        table_actions = (AddPolicyLink, DeletePolicyLink)
        row_actions = (AddFirewallLink, DeletePolicyLink)


class FirewallsTable(tables.DataTable):
    name = tables.Column("name",
                       verbose_name=_("Name"))

    class Meta:
        name = "firewallstable"
        verbose_name = _("Firewalls")
        table_actions = (DeleteFirewallLink,)
        row_actions = (DeleteFirewallLink,)

