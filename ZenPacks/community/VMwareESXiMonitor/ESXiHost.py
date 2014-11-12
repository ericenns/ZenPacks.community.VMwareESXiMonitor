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
from Products.ZenModel.Device import Device
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenModel.ZenossSecurity import ZEN_VIEW

class ESXiHost(Device):
    meta_type = portal_type = 'ESXiHost'

    cpuMhz = None
    cpuModel = None
    numCpuCores = None
    numCpuPkgs = None
    numCpuCoresPerPkgs = None
    numCpuThreads = None
    numNics = None
    esxiHostName = None
    vmotionState = False

    _properties = Device._properties + (
        {'id': 'cpuMhz', 'type': 'long'},
        {'id': 'cpuModel', 'type': 'string'},
        {'id': 'numCpuCores', 'type': 'int'},
        {'id': 'numCpuPkgs', 'type': 'int'},
        {'id': 'numCpuCoresPerPkgs', 'type': 'int'},
        {'id': 'numCpuThreads', 'type': 'int'},
        {'id': 'numNics', 'type': 'int'},
        {'id': 'esxiHostName', 'type': 'string'},
        {'id': 'vmotionState', 'type': 'boolean'},
    )

    _relations = Device._relations + (
        ('esxiVm', ToManyCont(ToOne,
            'ZenPacks.community.VMwareESXiMonitor.ESXiVM',
            'esxiHost',
            ),
        ),
        ('esxiDatastore', ToManyCont(ToOne,
            'ZenPacks.community.VMwareESXiMonitor.ESXiDatastore',
            'esxiHost',
            ),
        ),
    )

InitializeClass(ESXiHost)

