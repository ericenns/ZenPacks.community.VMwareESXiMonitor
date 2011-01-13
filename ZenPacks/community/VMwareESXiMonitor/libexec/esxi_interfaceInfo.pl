#!/usr/bin/perl
################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
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

my $host_view = Vim::find_entity_views(
	view_type => 'HostSystem'
);

my $host = @$host_view[0];

my $ifName;
my $description = "";
my $ipAddr;
my $mac;
my $type = "VMwareNic";
my $mtu;
my $status;
my $speed;
my $duplex;
my $index = 0;

foreach my $vnics (@{$host->config->network->vnic})
{
    $ifName = $vnics->device;
	$description = $vnics->portgroup;
    $ipAddr = $vnics->spec->ip->ipAddress;
    $mac = $vnics->spec->mac;
	$mtu = $vnics->spec->mtu;
	$status = 2;
	$speed = 0;
	$duplex = 0;
    print "$ifName;$status;$description;$ipAddr;$mac;$type;$mtu;$speed;$duplex;$index\n";
	$index++;
}

foreach my $pnics (@{$host->config->network->pnic})
{
	$ifName = $pnics->device;
	$description = "";
	if (exists $pnics->{linkSpeed})
	{
		$status = 1;
		$mtu = 0;
		$speed = $pnics->linkSpeed->speedMb;
		$duplex = $pnics->linkSpeed->duplex;
	}
	else
	{
		$status = 2;
		$mtu = 0;
		$speed = 0;
		$duplex = 0;
	}
	$ipAddr = $pnics->spec->ip->ipAddress;
	$mac = $pnics->mac;
	print "$ifName;$status;$description;$ipAddr;$mac;$type;$mtu;$speed;$duplex;$index\n";
	$index++;
}

Util::disconnect();
