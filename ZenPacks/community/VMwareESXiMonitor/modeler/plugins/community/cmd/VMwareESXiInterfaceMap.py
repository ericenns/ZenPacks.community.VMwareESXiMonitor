################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import Globals
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
import commands, re, os
from Products.DataCollector.plugins.DataMaps import ObjectMap

class VMwareESXiInterfaceMap(PythonPlugin):

	maptype = "InterfaceMap"
	compname = "os"
	relname = "interfaces"
	modname = "Products.ZenModel.IpInterface"
	deviceProperties = PythonPlugin.deviceProperties + ('zCommandUsername','zCommandPassword')

	def collect(self, device, log):
		log.info('Getting VMware ESXi interface info for device %s' % device.id)
		cmd = os.path.abspath('%s/../../../../libexec/esxi_interfaceInfo.pl' % os.path.dirname(__file__))
		username = getattr(device, 'zCommandUsername', None)
		password = getattr(device, 'zCommandPassword', None)
		if (not username or not password):
			return None
		(stat, output) = commands.getstatusoutput("/usr/bin/perl %s --server %s --username %s --password '%s'" % (cmd, device.id, username, password))
		if (stat != 0):
			return None
		else:
			results = output
			return results

	def process(self, device, results, log):
		log.info('Processing VMware ESXi interface info for device %s' % device.id)

		rm = self.relMap()

		rlines = results.split("\n")
		for line in rlines:
			if line.startswith("Warning:"):
				log.warning('%s' % line)
			elif re.search(';', line):
				ifName, ifStatus, ifDescription, ifIpAddr, ifMac, ifType, ifMtu, ifSpeed, ifDuplex, ifIndex = line.split(';')
				om = self.objectMap()
				om.id = ifName
				om.title = om.id
				om.interfaceName = om.id
				om.description = ifDescription
				om.type = ifType
				om.speed = ifSpeed
				om.mtu = ifMtu
				om.duplex = ifDuplex
				om.ifindex = ifIndex
				om.adminStatus = 1
				om.operStatus = ifStatus
				om.monitor = True
				if ifIpAddr:
					om.setIpAddresses = [ifIpAddr, ]
				om.macaddress = ifMac
				rm.append(om)
		log.debug(rm)

		return rm

