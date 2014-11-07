################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2014 Eric Enns, Matthias Kittl.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import Globals
import os.path
import logging
log = logging.getLogger('zen.vmwareesximonitor')

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import zenPath
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

_PACK_Z_PROPS = [
    ('zVSphereUsername', '', 'string'),
    ('zVSpherePassword', '', 'password'),
]

for name, default_value, type_ in _PACK_Z_PROPS:
    setzPropertyCategory(name, 'VMware')

class ZenPack(ZenPackBase):
    packZProperties = _PACK_Z_PROPS

    def install(self, app):
        if not hasattr(app.zport.dmd.Events.Status, 'VMware'):
            app.zport.dmd.Events.createOrganizer("/Status/VMware")
        app.zport.dmd.Reports.createOrganizer('/VMware Reports')
        ZenPackBase.install(self, app)
        log.info('Linking icon into $ZENHOME/Products/ZenWidgets/skins/zenui/img/icons')
        os.system('ln -sf %s %s' % (self.path('resources/img/icons/server-vmware.png'), zenPath('Products/ZenWidgets/skins/zenui/img/icons', 'server-vmware.png')))
        os.system('chmod 0644 %s' % (zenPath('Products/ZenWidgets/skins/zenui/img/icons', 'server-vmware.png')))

    def upgrade(self, app):
        if not hasattr(app.zport.dmd.Events.Status, 'VMware'):
            app.zport.dmd.Events.createOrganizer("/Status/VMware")
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            log.info('Removing icon from $ZENHOME/Products/ZenWidgets/skins/zenui/img/icons')
            os.system('rm -f %s' % (zenPath('Products/ZenWidgets/skins/zenui/img/icons', 'server-vmware.png')))
        ZenPackBase.remove(self, app, leaveObjects)

