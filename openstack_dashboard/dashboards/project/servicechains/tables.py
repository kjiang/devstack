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


class AddTemplateLink(tables.LinkAction):
    name = "addtemplate"
    verbose_name = _("Add Template")
    url = "horizon:project:servicechains:addtemplate"
    classes = ("btn-addtemplate",)


class AddChainLink(tables.LinkAction):
    name = "addchain"
    verbose_name = _("Create Chain from Template")
    classes = ("btn-addchain",)

    def get_link_url(self, template):
        base_url = reverse("horizon:project:servicechains:addchain",
                           kwargs={'template_id': template.id})
        return base_url


class DeleteTemplateLink(tables.DeleteAction):
    name = "deletetemplate"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Template")
    data_type_plural = _("Templates")


class DeleteChainLink(tables.DeleteAction):
    name = "deletechain"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Chain")
    data_type_plural = _("Chains")


class TemplatesTable(tables.DataTable):
    name = tables.Column("name",
                       verbose_name=_("Name"))
    class Meta:
        name = "templatestable"
        verbose_name = _("Templates")
        table_actions = (AddTemplateLink, DeleteTemplateLink)
        row_actions = (AddChainLink, DeleteTemplateLink)


class ChainsTable(tables.DataTable):
    name = tables.Column('name',
                            verbose_name=_("Name"))

    class Meta:
        name = "chainstable"
        verbose_name = _("Chains")
        table_actions = (DeleteChainLink,)
        row_actions = (DeleteChainLink,)

