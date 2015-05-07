################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2014 Eric Enns, Matthias Kittl.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """VMwareESXiDatastoreMap

VMwareESXiDatastoreMap gathers ESXi Datastore information.

"""

import re, commands, os
import Globals
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class VMwareESXiDatastoreMap(PythonPlugin):
    maptype = 'VMwareESXiDatastoreMap'
    relname = "esxiDatastore"
    modname = 'ZenPacks.community.VMwareESXiMonitor.ESXiDatastore'
    deviceProperties = PythonPlugin.deviceProperties + (
        'zVSphereUsername',
        'zVSpherePassword'
    )

    def collect(self, device, log):
        log.info('Getting VMware ESXi datastore info for device %s' % device.id)
        cmd = os.path.abspath('%s/../../../../libexec/esxi_datastoreinfo.pl' % os.path.dirname(__file__))
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
        log.info('Processing VMware ESXi datastore info for device %s' % device.id)
        rm = self.relMap()
        rlines = results.split("\n")
        for line in rlines:
            if line.startswith("Warning:"):
                log.warning('%s' % line)
            elif re.search(';', line):
                name, type, capacity, accessible = line.split(';')
                if not int(accessible) == 1:
                    log.warning('Datastore %s of device %s is not accessible' % (name, device.id))
                    continue
                rm.append(self.objectMap({
                    'id': self.prepId(name),
                    'title': name,
                    'type': type,
                    'capacity': long(capacity),
                }))
        log.debug(rm)

        return rm

