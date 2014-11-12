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
    properties => [ 'summary' ]
);

foreach my $host (@$host_views) {
    my $osVendor = $host->summary->config->product->vendor;
    my $osProduct = $host->summary->config->product->fullName;
    my $hwVendor = $host->summary->hardware->vendor;
    my $hwProduct = $host->summary->hardware->model;
    my $memorySize = $host->summary->hardware->memorySize;
    my $cpuMhz = $host->summary->hardware->cpuMhz;
    my $cpuModel = $host->summary->hardware->cpuModel;
    my $numCpuCores = $host->summary->hardware->numCpuCores;
    my $numCpuPkgs = $host->summary->hardware->numCpuPkgs;
    my $numCpuThreads = $host->summary->hardware->numCpuThreads;
    my $numNics = $host->summary->hardware->numNics;
    my $esxiHostName = $host->summary->config->name;
    my $vmotionState = $host->summary->config->vmotionEnabled;

    print $osVendor . ";" . $osProduct . ";" . $hwVendor . ";" . $hwProduct . ";" . $memorySize . ";" . $cpuMhz . ";" . $cpuModel . ";" . $numCpuCores . ";" . $numCpuPkgs . ";" . $numCpuThreads . ";" . $numNics . ";" . $esxiHostName . ";" . $vmotionState . "\n";
}

Util::disconnect();

