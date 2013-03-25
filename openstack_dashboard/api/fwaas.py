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


class Policy(QuantumAPIDictWrapper):
    """Wrapper for quantum firewall policy"""

    def __init__(self, apiresource):
        super(Policy, self).__init__(apiresource)

    class AttributeDict(dict):
        def __getattr__(self, attr):
            return self[attr]

        def __setattr__(self, attr, value):
            self[attr] = value

    def readable(self, request):
        pFormatted = {'id': self.id,
                      'name': self.name}

        return self.AttributeDict(pFormatted)


class Firewall(QuantumAPIDictWrapper):
    """Wrapper for quantum firewall"""

    def __init__(self, apiresource):
        super(Firewall, self).__init__(apiresource)

    class AttributeDict(dict):
        def __getattr__(self, attr):
            return self[attr]

        def __setattr__(self, attr, value):
            self[attr] = value

    def readable(self, request):
        mFormatted = {'id': self.id,
                      'name': self.name}

        return self.AttributeDict(mFormatted)


def policy_create(request, **kwargs):
    """Create a firewall policy

    :param request: request context
    :param name: policy name
    :returns: Policy object
    """
    body = {'policy': {'name': kwargs['name']}}
    #policy = quantumclient(request).create_policy(body).get('policy')
    policy = body
    return Policy(policy)


def policies_get(request, **kwargs):
    #policies = quantumclient(request).list_policies().get('policies')
    policies = []
    return [Policy(p) for p in policies]


def policy_get(request, policy_id):
    #policy = quantumclient(request).show_policy(policy_id).get('policy')
    policy = []
    return Policy(policy)


def policy_delete(request, policy_id):
    #quantumclient(request).delete_policy(policy_id)
    pass

def firewall_create(request, **kwargs):
    """Create a firewall for specified policy

    :param request: request context
    :param name: name for firewall
    """
    body = {'firewall': {'name': kwargs['name']}}
    #firewall = quantumclient(request).create_firewall(body).get('firewall')
    firewall = body
    return Firewall(firewall)


def firewalls_get(request, **kwargs):
    #firewalls = quantumclient(request).list_firewalls().get('firewalls')
    firewalls = []
    return [Firewall(f) for f in firewalls]


def firewall_get(request, firewall_id):
    #firewall = quantumclient(request).show_firewall(firewall_id).get('firewall')
    firewall = []
    return Firewall(firewall)


def firewall_delete(request, firewall):
    #quantumclient(request).delete_firewall(firewall)
    pass
