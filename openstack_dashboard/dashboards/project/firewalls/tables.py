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


class AddFirewallLink(tables.LinkAction):
    name = "addfirewall"
    verbose_name = _("Create Firewall")
    url = "horizon:project:firewalls:addfirewall"
    classes = ("btn-addfirewall",)


class ManageResourcesLink(tables.LinkAction):
    name = "manageresources"
    verbose_name = _("Manage Firewall Resources")
    url = "horizon:project:firewalls:managefirewall"
    classes = ("btn-managefirewall",)


class DeleteFirewallLink(tables.DeleteAction):
    name = "deletefirewall"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Firewall")
    data_type_plural = _("Firewalls")

    def action(self, request, obj_id):
        api.fwaas.firewall_delete(request, obj_id)


class RulesTable(tables.DataTable):
    description = tables.Column("description",
                                verbose_name=_("Description"))
    direction = tables.Column("direction",
                              verbose_name=_("Direction"))
    protocol = tables.Column("protocol",
                             verbose_name=_("Protocol"))
    source_ip_address = tables.Column("source_ip_address",
                                      verbose_name=_("Source"))
    destination_ip_address = tables.Column("destination_ip_address",
                                           verbose_name=_("Destination"))
    port_range = tables.Column("port_range",
                               verbose_name=_("Port Range"))
    application = tables.Column("application",
                                verbose_name=_("Application"))
    action = tables.Column("action",
                           verbose_name=_("Action"))
    dynamic_attributes = tables.Column("dynamic_attributes",
                                verbose_name=_("Dynamic Attributes"))
    class Meta:
        name = "rulestable"
        verbose_name = _("Rules")


class PoliciesTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"))
    description = tables.Column("description",
                                verbose_name=_("Description"))
    firewall_rules_list = tables.Column("firewall_rules_list",
                                   verbose_name=_("Firewall Rules"))
    class Meta:
        name = "policiestable"
        verbose_name = _("Policies")


class FirewallsTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:project:firewalls:firewalldetails")
    description = tables.Column("description",
                                verbose_name=_("Description"))
    firewall_policy_id = tables.Column("firewall_policy_id",
                                   verbose_name=_("Firewall Policy ID"))

    class Meta:
        name = "firewallstable"
        verbose_name = _("Firewalls")
        table_actions = (ManageResourcesLink, AddFirewallLink, DeleteFirewallLink)
        row_actions = (DeleteFirewallLink,)

