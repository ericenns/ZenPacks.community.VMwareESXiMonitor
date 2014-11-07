################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2014 Eric Enns, Matthias Kittl.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """VMwareESXiInterfaceMap

VMwareESXiInterfaceMap gathers ESXi Interface information.

"""

import re, commands, os
import Globals
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class VMwareESXiInterfaceMap(PythonPlugin):
    compname = "os"
    maptype = 'VMwareESXiInterfaceMap'
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"
    deviceProperties = PythonPlugin.deviceProperties + (
        'zVSphereUsername',
        'zVSpherePassword'
    )

    def collect(self, device, log):
        log.info('Getting VMware ESXi interface info for device %s' % device.id)
        cmd = os.path.abspath('%s/../../../../libexec/esxi_interfaceinfo.pl' % os.path.dirname(__file__))
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
        log.info('Processing VMware ESXi interface info for device %s' % device.id)
        rm = self.relMap()
        rlines = results.split("\n")
        for line in rlines:
            if line.startswith("Warning:"):
                log.warning('%s' % line)
            elif re.search(';', line):
                ifName, mac, type, description, mtu, speed, operStatus, duplex, ipAddr = line.split(';')
                om = self.objectMap()
                om.id = self.prepId(ifName)
                om.interfaceName = ifName
                om.ifindex = ifName
                om.macaddress = mac
                om.type = type
                om.description = description
                om.mtu = int(mtu)
                om.speed = long(speed)
                if int(operStatus) == 1:
                    om.adminStatus = 1
                    om.operStatus = 1
                elif int(operStatus) == 0:
                    om.adminStatus = 2
                    om.operStatus = 2
                om.duplex = int(duplex)
                if ipAddr:
                    om.setIpAddresses = ipAddr
                else:
                    om.setIpAddresses = []
                rm.append(om)

        log.debug(rm)

        return rm

