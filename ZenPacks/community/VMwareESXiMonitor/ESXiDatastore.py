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

class ESXiDatastore(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'ESXiDatastore'

    type = None
    capacity = None

    _properties = ManagedEntity._properties + (
        {'id': 'type', 'type': 'string'},
        {'id': 'capacity', 'type': 'long'},
    )

    _relations = ManagedEntity._relations + (
        ('esxiHost', ToOne(ToManyCont,
            'ZenPacks.community.VMwareESXiMonitor.ESXiHost',
            'esxiDatastore',
            ),
        ),
    )

    def device(self):
        return self.esxiHost()

    def usedSpace(self):
        capacity = self.capacity
        free = self.freeSpace()
        if capacity is None or free is None:
            return None
        return capacity - free

    def freeSpace(self):
        free = self.cacheRRDValue('diskFreeSpace')
        if free is None or isnan(free):
            return None
        return long(free)

    def usedPercent(self):
        capacity = self.capacity
        used = self.usedSpace()
        if capacity is None or used is None:
            return 'Unknown'
        return round(100.0 * used / capacity)

InitializeClass(ESXiDatastore)

