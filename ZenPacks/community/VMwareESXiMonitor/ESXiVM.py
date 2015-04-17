################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2014 Eric Enns, Matthias Kittl.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Globals import InitializeClass
from math import isnan
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS
from Products.ZenUtils.Utils import convToUnits

class ESXiVM(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'ESXiVM'

    osType = None
    memory = 0

    _properties = ManagedEntity._properties + (
        {'id': 'osType', 'type': 'string'},
        {'id': 'memory', 'type': 'int'},
    )

    _relations = ManagedEntity._relations + (
        ('esxiHost', ToOne(ToManyCont,
            'ZenPacks.community.VMwareESXiMonitor.ESXiHost',
            'esxiVm',
            ),
        ),
    )

    def device(self):
        return self.esxiHost()

    def adminStatus(self, default = None):
        status = self.cacheRRDValue('adminStatus', default)
        if status is not None and status != 'Unknown' and not isnan(status):
            return int(status)
        return None

    def operStatus(self, default = None):
        status = self.cacheRRDValue('operStatus', default)
        if status is not None and status != 'Unknown' and not isnan(status):
            return int(status)
        return None

InitializeClass(ESXiVM)

