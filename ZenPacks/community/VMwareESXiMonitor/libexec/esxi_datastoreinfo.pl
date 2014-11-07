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

my $datastore_views = Vim::find_entity_views(
    view_type => 'Datastore',
    properties => [ 'summary' ]
);

foreach my $datastore (@$datastore_views) {
    my $name = $datastore->summary->name;
    my $type = $datastore->summary->type;
    my $capacity = $datastore->summary->capacity;
    my $accessible = $datastore->summary->accessible;

    print $name . ";" . $type . ";" . $capacity . ";" . $accessible . "\n";
}

Util::disconnect();

