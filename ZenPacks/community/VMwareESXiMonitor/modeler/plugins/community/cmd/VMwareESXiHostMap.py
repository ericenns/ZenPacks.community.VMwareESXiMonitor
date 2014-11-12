################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2014 Eric Enns, Matthias Kittl.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """VMwareESXiHostMap

VMwareESXiHostMap gathers ESXi Host information.

"""

import commands, re, os
import Globals
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class VMwareESXiHostMap(PythonPlugin):
    maptype = "VMwareESXiHostMap"
    compname = ""
    deviceProperties = PythonPlugin.deviceProperties + (
        'zVSphereUsername',
        'zVSpherePassword'
    )

    def collect(self, device, log):
        log.info('Getting VMware ESXi host info for device %s' % device.id)
        cmd = os.path.abspath('%s/../../../../libexec/esxi_hostinfo.pl' % os.path.dirname(__file__))
        username = getattr(device, 'zVSphereUsername', None)
        password = getattr(device, 'zVSpherePassword', None)
        if (not username or not password):
            return None
        (stat, results) = commands.getstatusoutput( "/usr/bin/perl %s --server %s --username %s --password '%s'" % (cmd, device.id, username, password))
        if (stat != 0):
            return None
        else:
            return results

    def process(self, device, results, log):
        log.info('Processing VMware ESXi host info for device %s' % device.id)
        rlines = results.split("\n")
        for line in rlines:
            if line.startswith("Warning:"):
                log.warning('%s' % line)
            elif re.search(';', line):
                maps = []
                osVendor, osProduct, hwVendor, hwProduct, memorySize, cpuMhz, cpuModel, numCpuCores, numCpuPkgs, numCpuThreads, numNics, esxiHostName, vmotionState = line.split(';')
                maps.append(ObjectMap({'totalMemory': memorySize}, compname='hw'))
                maps.append(ObjectMap({'totalSwap': 0}, compname='os'))
                om = self.objectMap()
                om.setOSProductKey = osProduct
                om.setHWProductKey = hwProduct
                om.cpuMhz = long(cpuMhz)
                om.cpuModel = cpuModel
                om.numCpuCores = int(numCpuCores)
                om.numCpuPkgs = int(numCpuPkgs)
                om.numCpuCoresPerPkgs = int(numCpuCores) / int(numCpuPkgs)
                om.numCpuThreads = int(numCpuThreads)
                om.numNics = int(numNics)
                om.esxiHostName = esxiHostName
                if int(vmotionState) == 0:
                    om.vmotionState = True
                else:
                    om.vmotionState = False
                maps.append(om)

        return maps

