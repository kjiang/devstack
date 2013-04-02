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


class AddServiceChainLink(tables.LinkAction):
    name = "addchain"
    verbose_name = _("Create Chain")
    url = "horizon:project:servicechains:addchain"
    classes = ("btn-addchain",)


class DeleteServiceChainLink(tables.DeleteAction):
    name = "deletechain"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Chain")
    data_type_plural = _("Chains")


class ManageResourcesLink(tables.LinkAction):
    name = "managechain"
    verbose_name = _("Manage Resources")
    url = "horizon:project:servicechains:managechain"
    classes = ("btn-managechain",)


class TemplatesTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:project:servicechains:templatedetails")
    description = tables.Column("description",
                                verbose_name=_("Description"))
    service_types_list = tables.Column("service_types_list",
                                       verbose_name=_("Service Types"))

    class Meta:
        name = "templatestable"
        verbose_name = _("Templates")


class ServiceChainsTable(tables.DataTable):
    name = tables.Column('name',
                         verbose_name=_("Name"),
                         link="horizon:project:servicechains:chaindetails")
    description = tables.Column("description",
                                verbose_name=_("Description"))
    service_template_id = tables.Column("service_template_id",
                                        verbose_name=_("Service Template"))
    source_network = tables.Column("source_network",
                                   verbose_name=_("Source Network"))
    destination_network = tables.Column("destination_network",
                                        verbose_name=_("Destination Network"))
    services_list = tables.Column("services_list",
                                  verbose_name=_("Services"))

    class Meta:
        name = "chainstable"
        verbose_name = _("Chains")
        table_actions = (ManageResourcesLink, AddServiceChainLink, DeleteServiceChainLink)
        row_actions = (DeleteServiceChainLink,)
