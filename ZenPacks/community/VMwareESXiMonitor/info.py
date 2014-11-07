################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2014 Eric Enns, Matthias Kittl.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from zope.interface import implements
from Products.Zuul.infos import InfoBase, ProxyProperty
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.infos.component import ComponentInfo
from ZenPacks.community.VMwareESXiMonitor import interfaces
from Products.Zuul.utils import severityId

class ESXiHostInfo(DeviceInfo):
    implements(interfaces.IESXiHostInfo)

    cpuMhz = ProxyProperty('cpuMhz')
    cpuModel = ProxyProperty('cpuModel')
    numCpuCores = ProxyProperty('numCpuCores')
    numCpuPkgs = ProxyProperty('numCpuPkgs')
    numCpuCoresPerPkgs = ProxyProperty('numCpuCoresPerPkgs')
    numCpuThreads = ProxyProperty('numCpuThreads')
    numNics = ProxyProperty('numNics')
    vmotionState = ProxyProperty('vmotionState')


class VMwareDataSourceInfo(InfoBase):
    implements(interfaces.IVMwareDataSourceInfo)

    def __init__(self, dataSource):
        self._object = dataSource

    @property
    def testable(self):
        """
        This tells the client if we can test this datasource against a
        specific device.  It defaults to True and expects subclasses
        to overide it if they can not
        """
        return True

    @property
    def id(self):
        return '/'.join(self._object.getPrimaryPath())

    @property
    def source(self):
        return self._object.getDescription()

    @property
    def type(self):
        return self._object.sourcetype

    # severity
    def _setSeverity(self, value):
        try:
            if isinstance(value, str):
                value = severityId(value)
        except ValueError:
            # they entered junk somehow (default to info if invalid)
            value = severityId('info')
        self._object.severity = value

    def _getSeverity(self):
        return self._object.getSeverityString()

    @property
    def newId(self):
        return self._object.id

    severity = property(_getSeverity, _setSeverity)
    enabled = ProxyProperty('enabled')
    component = ProxyProperty('component')
    eventClass = ProxyProperty('eventClass')
    eventKey = ProxyProperty('eventKey')
    performanceSource = ProxyProperty('performanceSource')
    instance = ProxyProperty('instance')


class ESXiDatastoreInfo(ComponentInfo):
    implements(interfaces.IESXiDatastoreInfo)

    name = ProxyProperty('name')
    type = ProxyProperty('type')
    capacity = ProxyProperty('capacity')
    usedSpace = ProxyProperty('usedSpace')
    freeSpace = ProxyProperty('freeSpace')
    usedPercent = ProxyProperty('usedPercent')


class ESXiVMInfo(ComponentInfo):
    implements(interfaces.IESXiVMInfo)

    name = ProxyProperty('name')
    osType = ProxyProperty('osType')
    memory = ProxyProperty('memory')
    adminStatus = ProxyProperty('adminStatus')
    operStatus = ProxyProperty('operStatus')

