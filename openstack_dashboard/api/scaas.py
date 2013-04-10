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

from __future__ import absolute_import

from openstack_dashboard.api.quantum import QuantumAPIDictWrapper
from openstack_dashboard.api.quantum import quantumclient

import json

class ServiceChainTemplate(QuantumAPIDictWrapper):
    """Wrapper for quantum service chain template"""

    def __init__(self, apiresource):
        super(ServiceChainTemplate, self).__init__(apiresource)

    class AttributeDict(dict):
        def __getattr__(self, attr):
            return self[attr]

        def __setattr__(self, attr, value):
            self[attr] = value

    def readable(self, request):
        services_list_str = json.dumps(self.services_types_list)
        pFormatted = {'id': self.id,
                      'tenant_id': self.tenant_id,
                      'name': self.name,
                      'description': self.description,
                      'services_types_list': services_list_str}

        return self.AttributeDict(pFormatted)


class ServiceChain(QuantumAPIDictWrapper):
    """Wrapper for quantum service chain"""

    def __init__(self, apiresource):
        super(ServiceChain, self).__init__(apiresource)

    class AttributeDict(dict):
        def __getattr__(self, attr):
            return self[attr]

        def __setattr__(self, attr, value):
            self[attr] = value

    def readable(self, request):
        services_list_str = json.dumps(self.services_list)
        mFormatted = {'id': self.id,
                      'tenant_id': self.tenant_id,
                      'name': self.name,
                      'description': self.description,
                      'source_network_id': self.source_network_id,
                      'destination_network_id': self.destination_network_id,
                      'services_list': services_list_str}
        return self.AttributeDict(mFormatted)


def service_chain_template_create(request, **kwargs):
    """Create a service chain template

    :param request: request context
    :param name: template name
    :param description: temlate description
    :param services_types_list: list of service types in the template
    :returns: ServiceChainTemplate object
    """
    body = {'service_chain_template': {'name': kwargs['name'],
                                       'description': kwargs['description'],
                                       'services_types_list': kwargs['services_types_list']}}
    template = quantumclient(request).create_service_chain_template(body).get('service_chain_template')
    return ServiceChainTemplate(template)

def service_chain_templates_get(request, **kwargs):
    templates = quantumclient(request).list_service_chain_templates().get('service_chain_templates')
    return [ServiceChainTemplate(t) for t in templates]

def service_chain_template_get(request, template_id):
    template = quantumclient(request).show_service_chain_template(template_id).get('service_chain_template')
    return ServiceChainTemplate(template)

def service_chain_template_delete(request, template_id):
    quantumclient(request).delete_service_chain_template(template_id)

def service_chain_create(request, **kwargs):
    """Create a chain based on specified template

    :param request: request context
    :param name: name for service_chain
    :param description: description for service_chain
    :param template_id: id for service chain template
    :param source_network_id: source network string
    :param destination_network_id: destination network string
    :param services_list: list of services in the chain
    """
    body = {'service_chain': {'name': kwargs['name'],
                              'description': kwargs['description'],
                              'template_id': kwargs['template_id'],
                              'source_network_id': kwargs['source_network_id'],
                              'destination_network_id': kwargs['destination_network_id'],
                              'services_list': kwargs['services_list']}}
    chain = quantumclient(request).create_service_chain(body).get('service_chain')
    return ServiceChain(chain)

def service_chains_get(request, **kwargs):
    chains = quantumclient(request).list_service_chains().get('service_chains')
    return [ServiceChain(c) for c in chains]

def service_chain_get(request, chain_id):
    chain = quantumclient(request).show_service_chain(chain_id).get('service_chain')
    return ServiceChain(chain)

def service_chain_delete(request, chain):
    quantumclient(request).delete_service_chain(chain)

