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

class Rule(QuantumAPIDictWrapper):
    """Wrapper for quantum firewall policy"""

    def __init__(self, apiresource):
        super(Rule, self).__init__(apiresource)

    class AttributeDict(dict):
        def __getattr__(self, attr):
            return self[attr]

        def __setattr__(self, attr, value):
            self[attr] = value

    def readable(self, request):
        pFormatted = {'id': self.id,
                      'tenant_id': self.tenant_id,
                      'description': self.description,
                      'direction': self.direction,
                      'protocol': self.protocol,
                      'source_ip_address': self.source_ip_address,
                      'destination_ip_address': self.destination_ip_address,
                      'port_range_min': self.port_range_min,
                      'port_range_max': self.port_range_max,
                      'application': self.application,
                      'action': self.action,
                      'dynamic_attributes': self.dynamic_attributes}

        return self.AttributeDict(pFormatted)


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
                      'tenant_id': self.tenant_id,
                      'name': self.name,
                      'description': self.description,
                      'audited': self.audited}
        pFormatted['firewall_rules_list'] = []
        for f in self.firewall_rules_list:
            try:
                rule = firewall_rule_get(request, f)
                pFormatted['firewall_rules_list'].append( json.dumps(rule.description) )
            except:
                pass
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
                      'tenant_id': self.tenant_id,
                      'name': self.name,
                      'description': self.description,
                      'firewall_policy_id': self.firewall_policy_id,
                      'admin_state_up': self.admin_state_up,
                      'status': self.status}
        try:
            policy = firewall_policy_get(request, self.firewall_policy_id)
            mFormatted['firewall_policy_name'] = policy.name
        except:
            mFormatted['firewall_policy_name'] = self.firewall_policy_id

        return self.AttributeDict(mFormatted)

def firewall_rule_create(request, **kwargs):
    """Create a firewall rule

    :param request: request context
    :param description: description for firewall_rule
    :param direction: ingress or egress
    :param protocol: protocol
    :param source_ip_address: source ip address
    :param destination_ip_address: destination ip address
    :param port_range_min: port range min
    :param port_range_max: port range max
    :param application: application
    :param action: action
    :param dynamic_attributes: dynamic attributes
    :returns: firewall_rule object
    """
    body = {'firewall_rule': {'description': kwargs['description'],
                              'direction': kwargs['direction'],
                              'protocol': kwargs['protocol'],
                              'source_ip_address': kwargs['source_ip_address'],
                              'destination_ip_address': kwargs['destination_ip_address'],
                              'port_range_min': kwargs['port_range_min'],
                              'port_range_max': kwargs['port_range_max'],
                              'application': kwargs['application'],
                              'action': kwargs['action'],
                              'dynamic_attributes': kwargs['dynamic_attributes']
                              }}
    rule = quantumclient(request).create_firewall_rule(body).get('firewall_rule')
    return Rule(rule)

def firewall_rules_get(request, **kwargs):
    rules = quantumclient(request).list_firewall_rules().get('firewall_rules')
    return [Rule(r) for r in rules]

def firewall_rule_get(request, rule_id):
    rule = quantumclient(request).show_firewall_rule(rule_id).get('firewall_rule')
    return Rule(rule)

def firewall_rule_delete(request, rule_id):
    quantumclient(request).delete_firewall_rule(rule_id)

def firewall_policy_create(request, **kwargs):
    """Create a firewall policy

    :param request: request context
    :param name: name for firewall_policy
    :param description: description for firewall_policy
    :param firewall_rules_list: list of firewall_rules for firewall_policy
    :returns: firewall_policy object
    """
    body = {'firewall_policy': {'name': kwargs['name'],
                                'description': kwargs['description'],
                                'firewall_rules_list': kwargs['firewall_rules_list'],
                                'audited': kwargs['audited']
                                }}
    policy = quantumclient(request).create_firewall_policy(body).get('firewall_policy')
    return Policy(policy)

def firewall_policies_get(request, **kwargs):
    policies = quantumclient(request).list_firewall_policies().get('firewall_policies')
    return [Policy(p) for p in policies]

def firewall_policy_get(request, policy_id):
    policy = quantumclient(request).show_firewall_policy(policy_id).get('firewall_policy')
    return Policy(policy)

def firewall_policy_delete(request, policy_id):
    quantumclient(request).delete_firewall_policy(policy_id)

def firewall_create(request, **kwargs):
    """Create a firewall

    :param request: request context
    :param name: name for firewall
    :param description: description for firewall
    :param firewall_policy_id: firewall policy id
    :param admin_state_up: admin state up
    :returns: firewall object
    """
    body = {'firewall': {'name': kwargs['name'],
                         'description': kwargs['description'],
                         'firewall_policy_id': kwargs['firewall_policy_id'],
                         'admin_state_up': kwargs['admin_state_up']
                         }}
    firewall = quantumclient(request).create_firewall(body).get('firewall')
    return Firewall(firewall)

def firewalls_get(request, **kwargs):
    firewalls = quantumclient(request).list_firewalls().get('firewalls')
    return [Firewall(f) for f in firewalls]

def firewall_get(request, firewall_id):
    firewall = quantumclient(request).show_firewall(firewall_id).get('firewall')
    return Firewall(firewall)

def firewall_delete(request, firewall_id):
    quantumclient(request).delete_firewall(firewall_id)
