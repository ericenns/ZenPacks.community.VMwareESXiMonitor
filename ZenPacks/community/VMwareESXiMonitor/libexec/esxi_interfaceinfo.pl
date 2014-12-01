#!/usr/bin/perl
################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2014 Eric Enns, Matthias Kittl.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

use strict;
use warnings;
use VMware::VIRuntime;

Opts::parse();
Opts::validate();

Util::connect();

my $host_views = Vim::find_entity_views(
    view_type => 'HostSystem',
    properties => [ 'config.network' ]
);

foreach my $host (@$host_views) {
    my $ifName;
    my $mac;
    my $type;
    my $description;
    my $mtu;
    my $speed;
    my $operStatus;
    my $duplex;
    my $ipAddr;

    foreach my $vnic (@{$host->get_property('config.network')->vnic}) {
        $ifName = $vnic->device;
        $mac = $vnic->spec->mac;
        $type = "Virtual Adapter";
        $description = $vnic->portgroup;
        $mtu = $vnic->spec->mtu;
        $speed = 0;
        $operStatus = 1;
        $duplex = 0;
        $ipAddr = $vnic->spec->ip->ipAddress;

        print "$ifName;$mac;$type;$description;$mtu;$speed;$operStatus;$duplex;$ipAddr\n";
    }

    foreach my $pnic (@{$host->get_property('config.network')->pnic}) {
        $ifName = $pnic->device;
        $mac = $pnic->mac;
        $type = "Physical Adapter";
        $description = "";
        $mtu = 0;
        if (exists $pnic->{linkSpeed}) {
            $speed = $pnic->linkSpeed->speedMb;
            $operStatus = 1;
            $duplex = $pnic->linkSpeed->duplex;
        }
        else {
            $speed = 0;
            $operStatus = 0;
            $duplex = 0;
        }
        $ipAddr = $pnic->spec->ip->ipAddress;

        print "$ifName;$mac;$type;$description;$mtu;$speed;$operStatus;$duplex;$ipAddr\n";
    }
}

Util::disconnect();

