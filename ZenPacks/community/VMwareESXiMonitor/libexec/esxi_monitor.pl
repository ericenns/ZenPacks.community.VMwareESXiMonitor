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

my %opts = (
    options => {
        type => "=s",
        variable => "VI_OPTIONS",
        help => "Query Options",
        required => 1,
    },
);

Opts::add_options(%opts);
Opts::parse();
Opts::validate();

Util::connect();

my $options = Opts::get_option('options');

eval {
    Util::connect();

    if ($options =~ /^datastoreperf:(.*)$/) {
        my $datastore_name = {name => $1};
        my $datastore_view = Vim::find_entity_views(view_type => 'Datastore', filter => $datastore_name, properties => [ 'summary' ]);
        die "Runtime error\n" if (!defined($datastore_view));
        die "Datastore \"" . $$datastore_name{"name"} . "\" does not exist\n" if (!@$datastore_view);
        if (!($$datastore_view[0]->summary->accessible)) {
            print "datastoreperf|diskFreeSpace= connectionStatus=2\n";
        }
        else {
            my $diskFreeSpace = $$datastore_view[0]->summary->freeSpace;

            print "datastoreperf|diskFreeSpace=".$diskFreeSpace." connectionStatus=1\n";
        }
    }
    elsif ($options =~ /^guestperf:(.*)$/) {
        my $vm_name = $1;
        my $vm_view = Vim::find_entity_views(view_type => 'VirtualMachine', filter => {name => $vm_name}, properties => [ 'name', 'runtime.powerState', 'summary.overallStatus' ]);
        die "Runtime error\n" if (!defined($vm_view));
        die "VMware machine \"" . $vm_name . "\" does not exist\n" if (!@$vm_view);
        my $powerState = $$vm_view[0]->get_property('runtime.powerState')->val;
        if ($powerState ne "poweredOn") {
            my $adminStatus = 0;
            if ($powerState eq "poweredOff") {
                $adminStatus = 2;
            }
            elsif ($powerState eq "suspended") {
                $adminStatus = 3;
            }

            print "guestperf|memUsage= memOverhead= memConsumed= diskUsage= cpuUsageMin= cpuUsageMax= cpuUsageAvg= cpuUsage= adminStatus=".$adminStatus." operStatus=0\n";
        }
        else {
            my $perfmgr_view = Vim::get_view(mo_ref => Vim::get_service_content()->perfManager, properties => [ 'perfCounter' ]);
            my $memUsage = get_info($vm_view, $perfmgr_view, 'mem', 'usage', 'minimum');
            my $memOverhead = get_info($vm_view, $perfmgr_view, 'mem', 'overhead', 'minimum');
            my $memConsumed = get_info($vm_view, $perfmgr_view, 'mem', 'consumed', 'minimum');
            my $diskUsage = get_info($vm_view, $perfmgr_view, 'disk', 'usage', 'average');
            my $cpuUsageMin = get_info($vm_view, $perfmgr_view, 'cpu', 'usage', 'minimum');
            my $cpuUsageMax = get_info($vm_view, $perfmgr_view, 'cpu', 'usage', 'maximum');
            my $cpuUsageAvg = get_info($vm_view, $perfmgr_view, 'cpu', 'usage', 'average');
            my $cpuUsage = get_info($vm_view, $perfmgr_view, 'cpu', 'usagemhz', 'average');

            my $overallStatus = $$vm_view[0]->get_property('summary.overallStatus')->val;
            my $operStatus = 0;
            if ($overallStatus eq "green") {
                $operStatus = 1;
            }
            elsif ($overallStatus eq "red") {
                $operStatus = 2;
            }
            elsif ($overallStatus eq "yellow") {
                $operStatus = 3;
            }
            elsif ($overallStatus eq "gray") {
                $operStatus = 4;
            }

            print "guestperf|memUsage=".$memUsage." memOverhead=".$memOverhead." memConsumed=".$memConsumed." diskUsage=".$diskUsage." cpuUsageMin=".$cpuUsageMin." cpuUsageMax=".$cpuUsageMax." cpuUsageAvg=".$cpuUsageAvg." cpuUsage=".$cpuUsage." adminStatus=1 operStatus=".$operStatus."\n";
        }
    }
    elsif ($options =~ /^hostperf:(.*)$/) {
        my $host_name = {name => $1};
        my $host_view = Vim::find_entity_views(view_type => 'HostSystem', filter => $host_name, properties => [ 'name', 'runtime.inMaintenanceMode' ]);
        die "Runtime error\n" if (!defined($host_view));
        die "Host \"" . $$host_name{"name"} . "\" does not exist\n" if (!@$host_view);
        if (uc($$host_view[0]->get_property('runtime.inMaintenanceMode')) eq "TRUE") {
            print "hostperf|sysUpTime= memSwapused= memGranted= memActive= diskUsage= cpuUsagemhz= cpuUsage= cpuReservedcapacity= netReceived= netTransmitted= netPacketsRx= netPacketsTx= netDroppedRx= netDroppedTx=\n";
        }
        else {
            my $perfmgr_view = Vim::get_view(mo_ref => Vim::get_service_content()->perfManager, properties => [ 'perfCounter' ]);
            my $sysUpTime = get_info($host_view, $perfmgr_view, 'sys', 'uptime', 'latest') * 100;
            my $memSwapused = get_info($host_view, $perfmgr_view, 'mem', 'swapused', 'maximum');
            my $memGranted = get_info($host_view, $perfmgr_view, 'mem', 'granted', 'maximum');
            my $memActive = get_info($host_view, $perfmgr_view, 'mem', 'active', 'maximum');
            my $diskUsage = get_info($host_view, $perfmgr_view, 'disk', 'usage', 'average');
            my $cpuUsagemhz = get_info($host_view, $perfmgr_view, 'cpu', 'usagemhz', 'average');
            my $cpuUsage = get_info($host_view, $perfmgr_view, 'cpu', 'usage', 'average');
            my $cpuReservedcapacity = get_info($host_view, $perfmgr_view, 'cpu', 'reservedCapacity', 'average');
            my $netReceived = get_info($host_view, $perfmgr_view, 'net', 'received', 'average');
            my $netTransmitted = get_info($host_view, $perfmgr_view, 'net', 'transmitted', 'average');
            my $netPacketsRx = get_info($host_view, $perfmgr_view, 'net', 'packetsRx', 'summation');
            my $netPacketsTx = get_info($host_view, $perfmgr_view, 'net', 'packetsTx', 'summation');
            my $netDroppedRx = get_info($host_view, $perfmgr_view, 'net', 'droppedRx', 'summation');
            my $netDroppedTx = get_info($host_view, $perfmgr_view, 'net', 'droppedTx', 'summation');

            print "hostperf|sysUpTime=".$sysUpTime." memSwapused=".$memSwapused." memGranted=".$memGranted." memActive=".$memActive." diskUsage=".$diskUsage." cpuUsagemhz=".$cpuUsagemhz." cpuUsage=".$cpuUsage." cpuReservedcapacity=".$cpuReservedcapacity." netReceived=".$netReceived." netTransmitted=".$netTransmitted." netPacketsRx=".$netPacketsRx." netPacketsTx=".$netPacketsTx." netDroppedRx=".$netDroppedRx." netDroppedTx=".$netDroppedTx."\n";
        }
    }
};

Util::disconnect();

###############################################################################

sub get_key_metrices {
    my ($perfmgr_view, $group, @names) = @_;
    my $perfCounterInfo = $perfmgr_view->perfCounter;
    my @counters;

    foreach (@$perfCounterInfo) {
        if ($_->groupInfo->key eq $group) {
            my $cur_name = $_->nameInfo->key . "." . $_->rollupType->val;
            foreach my $index (0..@names-1) {
                if ($names[$index] =~ /$cur_name/) {
                    $names[$index] =~ /(\w+).(\w+):*(.*)/;
                    $counters[$index] = PerfMetricId->new(counterId => $_->key, instance => $3);
                }
            }
        }
    }
    return \@counters;
}

sub get_performance_values {
    my ($views, $perfmgr_view, $group, @list) = @_;
    my $counter = 0;
    my @values = ();
    my $amount = @list;
    eval {
        my $metrices = get_key_metrices($perfmgr_view, $group, @list);

        my @perf_query_spec = ();
        push(@perf_query_spec, PerfQuerySpec->new(entity => $_, metricId => $metrices, format => 'csv', intervalId => 20, maxSample => 1)) foreach (@$views);
        my $perf_data = $perfmgr_view->QueryPerf(querySpec => \@perf_query_spec);
        $amount *= @$perf_data;

        while (@$perf_data) {
            my $unsorted = shift(@$perf_data)->value;
            my @host_values = ();

            foreach my $id (@$unsorted) {
                foreach my $index (0..@$metrices-1) {
                    if ($id->id->counterId == $$metrices[$index]->counterId) {
                        $counter++ if (!defined($host_values[$index]));
                        $host_values[$index] = $id;
                    }
                }
            }
            push(@values, \@host_values);
        }
    };
    return undef if ($@ || $counter != $amount);
    return \@values;
}

sub get_info {
    my ($views, $perfmgr_view, $group_type, $counter, $rollup_type) = @_;
    my $values;
    $values = get_performance_values($views, $perfmgr_view, $group_type, ($counter.".".$rollup_type));

    if (defined($values)) {
        my ( $t ) = split(/,/, $$values[0][0]->value);
        return $t;
    }
}

