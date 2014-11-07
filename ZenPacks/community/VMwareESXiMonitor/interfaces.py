################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2014 Eric Enns, Matthias Kittl.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.Zuul.form import schema
from Products.Zuul.interfaces.device import IDeviceInfo
from Products.Zuul.interfaces.component import IInfo, IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

class IESXiHostInfo(IDeviceInfo):
    cpuMhz = schema.TextLine(title=_t(u'CPU MHz'))
    cpuModel = schema.TextLine(title=_t(u'Processor Type'))
    numCpuCores = schema.TextLine(title=_t(u'CPU Cores'))
    numCpuPkgs = schema.TextLine(title=_t(u'Processor Sockets'))
    numCpuCoresPerPkgs = schema.TextLine(title=_t(u'Cores per Socket'))
    numCpuThreads = schema.TextLine(title=_t(u'Logical Processors'))
    numNics = schema.TextLine(title=_t(u'Number of NICs'))
    vmotionState = schema.TextLine(title=_t(u'vMotion Enabled'))


class IVMwareDataSourceInfo(IInfo):
    newId = schema.TextLine(
        title=_t(u'Name'),
        xtype="idfield",
        description=_t(u'The name of this datasource')
    )
    type = schema.TextLine(
        title=_t(u'Type'),
        readonly=True
    )
    enabled = schema.Bool(title=_t(u'Enabled'))
    severity = schema.TextLine(
        title=_t(u'Severity'),
        xtype='severity'
    )
    eventKey = schema.TextLine(title=_t(u'Event Key'))
    eventClass = schema.TextLine(
        title=_t(u'Event Class'),
        xtype='eventclass'
    )
    component = schema.TextLine(title=_t(u'Component'))
    instance = schema.TextLine(title=_t(u'Instance'))
    performanceSource = schema.TextLine(
        title=_t(u'Performance Source'),
        group="Counter Group"
    )
    instance = schema.TextLine(
        title=_t(u'Instance'),
        group="Counter Group"
    )


class IESXiDatastoreInfo(IComponentInfo):
    name = schema.TextLine(title=_t(u'Name'))
    type = schema.TextLine(title=_t(u'Type'))
    capacity = schema.TextLine(title=_t(u'Capacity Bytes'))
    usedSpace = schema.TextLine(title=_t(u'Used Space Bytes'))
    freeSpace = schema.TextLine(title=_t(u'Free Space Bytes'))
    usedPercent = schema.TextLine(title=_t(u'Used Percent'))


class IESXiVMInfo(IComponentInfo):
    name = schema.TextLine(title=_t(u'Name'))
    osType = schema.TextLine(title=_t(u'Operating System Type'))
    memory = schema.TextLine(title=_t(u'Memory Bytes'))
    adminStatus = schema.TextLine(title=_t(u'Admin Status'))
    operStatus = schema.TextLine(title=_t(u'Operating Status'))

