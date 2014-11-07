(function() {
    var ZC = Ext.ns('Zenoss.component');

    Ext.define("Zenoss.component.ESXiDatastorePanel", {
        alias:['widget.ESXiDatastorePanel'],
        extend:"Zenoss.component.ComponentGridPanel",
        constructor: function(config) {
            config = Ext.applyIf(config||{}, {
                autoExpandColumn: 'name',
                componentType: 'ESXiDatastore',
                fields: [
                    {name: 'uid'},
                    {name: 'name'},
                    {name: 'status'},
                    {name: 'severity'},
                    {name: 'usesMonitorAttribute'},
                    {name: 'monitor'},
                    {name: 'monitored'},
                    {name: 'locking'},
                    {name: 'type'},
                    {name: 'capacity'},
                    {name: 'usedSpace'},
                    {name: 'freeSpace'},
                    {name: 'usedPercent'}
                ],
                columns: [{
                    id: 'severity',
                    dataIndex: 'severity',
                    header: _t('Events'),
                    renderer: Zenoss.render.severity,
                    width: 60
                },{
                    id: 'name',
                    dataIndex: 'name',
                    header: _t('Name'),
                    sortable: true
                },{
                    id: 'type',
                    dataIndex: 'type',
                    header: _t('Type'),
                    sortable: true
                },{
                    id: 'capacity',
                    dataIndex: 'capacity',
                    header: _t('Capacity'),
                    renderer: Zenoss.render.bytesString,
                    sortable: true
                },{
                    id: 'usedSpace',
                    dataIndex: 'usedSpace',
                    header: _t('Used Space'),
                    renderer: function(n) {
                        if (n<0) {
                            return _t('Unknown');
                        } else {
                            return Zenoss.render.bytesString(n);
                        }
                    },
                    sortable: true
                },{
                    id: 'freeSpace',
                    dataIndex: 'freeSpace',
                    header: _t('Free Space'),
                    renderer: function(n) {
                        if (n<0) {
                            return _t('Unknown');
                        } else {
                            return Zenoss.render.bytesString(n);
                        }
                    },
                    sortable: true
                },{
                    id: 'usedPercent',
                    dataIndex: 'usedPercent',
                    header: _t('% Util'),
                    renderer: function(n) {
                        if (n=='Unknown' || n<0) {
                            return _t('Unknown');
                        } else {
                            return n + '%';
                        }
                    },
                    sortable: true
                },{
                    id: 'monitored',
                    dataIndex: 'monitored',
                    header: _t('Monitored'),
                    renderer: Zenoss.render.checkbox,
                    width: 60
                },{
                    id: 'locking',
                    dataIndex: 'locking',
                    header: _t('Locking'),
                    renderer: Zenoss.render.locking_icons
                }]
            });
            ZC.ESXiDatastorePanel.superclass.constructor.call(this, config);
        }
    });

    ZC.registerName('ESXiDatastore', _t('ESXi Datastore'), _t('ESXi Datastores'));

    Ext.define("Zenoss.component.ESXiVMPanel", {
        alias:['widget.ESXiVMPanel'],
        extend:"Zenoss.component.ComponentGridPanel",
        constructor: function(config) {
            config = Ext.applyIf(config||{}, {
                autoExpandColumn: 'osType',
                componentType: 'ESXiVM',
                fields: [
                    {name: 'uid'},
                    {name: 'name'},
                    {name: 'status'},
                    {name: 'severity'},
                    {name: 'usesMonitorAttribute'},
                    {name: 'monitor'},
                    {name: 'monitored'},
                    {name: 'locking'},
                    {name: 'osType'},
                    {name: 'memory'},
                    {name: 'adminStatus'},
                    {name: 'operStatus'}
                ],
                columns: [{
                    id: 'severity',
                    dataIndex: 'severity',
                    header: _t('Events'),
                    renderer: Zenoss.render.severity,
                    width: 60
                },{
                    id: 'name',
                    dataIndex: 'name',
                    header: _t('Name'),
                    sortable: true
                },{
                    id: 'osType',
                    dataIndex: 'osType',
                    header: _t('Operating System Type'),
                    sortable: true
                },{
                    id: 'memory',
                    dataIndex: 'memory',
                    header: _t('Memory'),
                    renderer: Zenoss.render.bytesString,
                    sortable: true
                },{
                    id: 'adminStatus',
                    dataIndex: 'adminStatus',
                    header: _t('Admin Status'),
                    renderer: function(n) {
                        var tpl = new Ext.Template(
                            '<img border="0" src="img/{color}_dot.png"',
                            'style="vertical-align:middle"/>'
                        ),
                        result = '';
                        tpl.compile();
                        switch (n) {
                            case 1:
                                result += tpl.apply({color:'green'});
                                break;
                            case 2:
                                result += tpl.apply({color:'red'});
                                break;
                            case 3:
                                result += tpl.apply({color:'orange'});
                                break;
                            default:
                                result += tpl.apply({color:'blue'});
                        }
                        return result;
                    },
                    sortable: true
                },{
                    id: 'operStatus',
                    dataIndex: 'operStatus',
                    header: _t('Operating Status'),
                    renderer: function(n, meta, record) {
                        var adminStatus = record.data.adminStatus;
                        var tpl = new Ext.Template(
                            '<img border="0" src="img/{color}_dot.png"',
                            'style="vertical-align:middle"/>'
                        ),
                        result = '';
                        tpl.compile();
                        if (adminStatus==1) {
                            switch (n) {
                                case 1:
                                    result += tpl.apply({color:'green'});
                                    break;
                                case 2:
                                    result += tpl.apply({color:'red'});
                                    break;
                                case 3:
                                    result += tpl.apply({color:'yellow'});
                                    break;
                                case 4:
                                    result += tpl.apply({color:'grey'});
                                    break;
                                default:
                                    result += tpl.apply({color:'blue'});
                            }
                        } else {
                            result += tpl.apply({color:'grey'});
                        }
                        return result;
                    },
                    sortable: true
                },{
                    id: 'monitored',
                    dataIndex: 'monitored',
                    header: _t('Monitored'),
                    renderer: Zenoss.render.checkbox,
                    width: 60
                },{
                    id: 'locking',
                    dataIndex: 'locking',
                    header: _t('Locking'),
                    renderer: Zenoss.render.locking_icons
                }]
            });
            ZC.ESXiVMPanel.superclass.constructor.call(this, config);
        }
    });

    ZC.registerName('ESXiVM', _t('ESXi VM'), _t('ESXi VMs'));

    Ext.onReady(function() {
        var DEVICE_SNMP_ID = 'deviceoverviewpanel_snmpsummary';
        Ext.ComponentMgr.onAvailable(DEVICE_SNMP_ID, function() {
            var snmp = Ext.getCmp(DEVICE_SNMP_ID);
            snmp.removeField('snmpSysName');
            snmp.removeField('snmpLocation');
            snmp.removeField('snmpContact');
            snmp.removeField('snmpDescr');
            snmp.removeField('snmpCommunity');
            snmp.removeField('snmpVersion');
            snmp.addField({
                xtype: 'displayfield',
                id: 'cpu-mhz-displayfield',
                name: 'cpuMhz',
                fieldLabel: _t('CPU MHz')
            });
            snmp.addField({
                xtype: 'displayfield',
                id: 'cpu-model-displayfield',
                name: 'cpuModel',
                fieldLabel: _t('Processor Type')
            });
            snmp.addField({
                xtype: 'displayfield',
                id: 'num-cpu-cores-displayfield',
                name: 'numCpuCores',
                fieldLabel: _t('CPU Cores')
            });
            snmp.addField({
                xtype: 'displayfield',
                id: 'num-cpu-pkgs-displayfield',
                name: 'numCpuPkgs',
                fieldLabel: _t('Processor Sockets')
            });
            snmp.addField({
                xtype: 'displayfield',
                id: 'num-cpu-cores-per-pkgs-displayfield',
                name: 'numCpuCoresPerPkgs',
                fieldLabel: _t('Cores per Socket')
            });
            snmp.addField({
                xtype: 'displayfield',
                id: 'num-cpu-threads-displayfield',
                name: 'numCpuThreads',
                fieldLabel: _t('Logical Processors')
            });
            snmp.addField({
                xtype: 'displayfield',
                id: 'num-nics-displayfield',
                name: 'numNics',
                fieldLabel: _t('Number of NICs')
            });
            snmp.addField({
                xtype: 'displayfield',
                id: 'vmotion-state-displayfield',
                name: 'vmotionState',
                fieldLabel: _t('vMotion Enabled')
            });
        });
    });
})();

