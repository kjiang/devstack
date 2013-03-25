from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import horizon

from openstack_dashboard.dashboards.project import dashboard


class ServiceChain(horizon.Panel):
    name = _("Service Chains")
    slug = "servicechains"
    permissions = ('openstack.services.network',)


if getattr(settings, 'OPENSTACK_QUANTUM_NETWORK', {}).get('enable_lb', False):
    dashboard.Project.register(ServiceChain)
