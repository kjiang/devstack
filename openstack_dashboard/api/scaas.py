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


class Template(QuantumAPIDictWrapper):
    """Wrapper for quantum service chain template"""

    def __init__(self, apiresource):
        super(Template, self).__init__(apiresource)

    class AttributeDict(dict):
        def __getattr__(self, attr):
            return self[attr]

        def __setattr__(self, attr, value):
            self[attr] = value

    def readable(self, request):
        pFormatted = {'id': self.id,
                      'name': self.name}

        return self.AttributeDict(pFormatted)


class Chain(QuantumAPIDictWrapper):
    """Wrapper for quantum service chain"""

    def __init__(self, apiresource):
        super(Chain, self).__init__(apiresource)

    class AttributeDict(dict):
        def __getattr__(self, attr):
            return self[attr]

        def __setattr__(self, attr, value):
            self[attr] = value

    def readable(self, request):
        mFormatted = {'id': self.id,
                      'name': self.name}

        return self.AttributeDict(mFormatted)


def template_create(request, **kwargs):
    """Create a service chain template

    :param request: request context
    :param name: template name
    :returns: Template object
    """
    body = {'template': {'name': kwargs['name']}}
    #template = quantumclient(request).create_template(body).get('template')
    template = body
    return Template(template)


def templates_get(request, **kwargs):
    #templates = quantumclient(request).list_templates().get('templates')
    templates = []
    return [Template(t) for t in templates]


def template_get(request, template_id):
    #template = quantumclient(request).show_template(template_id).get('template')
    template = []
    return Template(template)


def template_delete(request, template_id):
    #quantumclient(request).delete_template(template_id)
    pass

def chain_create(request, **kwargs):
    """Create a chain based on specified template

    :param request: request context
    :param name: name for chain
    """
    body = {'chain': {'name': kwargs['name']}}
    #chain = quantumclient(request).create_chain(body).get('chain')
    chain = body
    return Chain(chain)


def chains_get(request, **kwargs):
    #chains = quantumclient(request).list_chains().get('chains')
    chains = []
    return [Chain(c) for c in chains]


def chain_get(request, chain_id):
    #chain = quantumclient(request).show_chain(chain_id).get('chain')
    chain = []
    return Chain(chain)


def chain_delete(request, chain):
    #quantumclient(request).delete_chain(chain)
    pass
