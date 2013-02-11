#!/bin/sh
#
# Submits an OSSEC alert as a passive service check result to zabbix.
#
# Author: David M. Zendzian
# ZZ Servers, LLC 2010
# 
# Idea from Dave Stycos post: http://groups.google.com/group/ossec-dev/browse_thread/thread/e29c5d71926b8af5
#
# This script is Public Domain, and is provided AS-IS.  There is no
# warranty, and no support given for its contents.
#
# Version 1.0: Apr. 6, 2010
#

DEBUG="false"
ACTION=$1
USER=$2
IP=$3
ALERTID=$4
RULEID=$5

LOCAL=`dirname $0`;
cd $LOCAL
cd ../
PWD=`pwd`
UNAME=`uname`

# Zabbix Sender
ZabbixSender="/usr/bin/zabbix_sender"
#ZabbixSender="/usr/sbin/zabbix_sender"

# Zabbix Server
ZabbixServer=10.252.5.169

# Zabbix Port
ZabbixPort=10051

# All alerts will be processed by Zabbix under this key.
ZabbixKeyName=OSSEC

# Check that zabbix_sender file exists.
if [ ! -w $ZabbixSender ]; then
    logger -p local0.err "$0: File $ZabbixSender not found.  Exiting."
    exit 1
fi

# Getting alert time
ALERTTIME=`echo "$ALERTID" | cut -d  "." -f 1`

# Getting end of alert
ALERTLAST=`echo "$ALERTID" | cut -d  "." -f 2`

# Getting full alert
ALERTTEXT=`grep -A 10 "$ALERTTIME" $PWD/../logs/alerts/alerts.log | grep -v ".$ALERTLAST: " -A 10 `

# Extract host (agent) name from alert.
HOSTNAME=`echo "$ALERTTEXT" | sed -n '1,1s/^.*\:[0-9][0-9]\:[0-9][0-9][^A-Za-z0-9_]*\([-A-Za-z0-9_]*\)\->.*$/\1/p'`

# if hostname alert wasn't from local host, the host value is "(hostname) ip", which extracts differently
if [ "$HOSTNAME" = "" ]
then
HOSTNAME=`echo "$ALERTTEXT" | sed -n '1,1s/^.*\:[0-9][0-9]\:[0-9][0-9] (\([-A-Za-z0-9_]*\)) .*\->.*$/\1/p'`
fi
if [ "$HOSTNAME" = "" ]
then
exit 0
fi

# Extract alert level from alert.
ALERTLVL=`echo "$ALERTTEXT" | sed -n '2,2s/^.*(level \([0-9]*\).*$/\1/p'`

# Extract description from alert.
ALERTMSG=`echo "$ALERTTEXT" | sed -n '5,5p'`

# Create Alert message
ZMSG="AlertID: $ALERTID | User: $USER | IP: $IP | Level: $ALERTLVL | RuleID: $RULEID - $ALERTMSG"

# Send result to zabbix for logging and notification alerts.
$ZabbixSender --zabbix-server $ZabbixServer --port $ZabbixPort --host $HOSTNAME --key $ZabbixKeyName --value "$ZMSG"

if [ "$DEBUG" = "true" ]
then
echo "$ZabbixSender --zabbix-server $ZabbixServer --port $ZabbixPort --host $HOSTNAME --key $ZabbixKeyName --value '$ZMSG'" >> /tmp/zabbix-test.log
echo "ACTION: $ACTION" >> /tmp/zabbix-test.log
echo "USER: $USER"
echo "IP: $IP" >> /tmp/zabbix-test.log
echo "ALERTID: $ALERTID" >> /tmp/zabbix-test.log
echo "ALERTLVL: $ALERTLVL" >> /tmp/zabbix-test.log
echo "RULEID: $RULEID" >> /tmp/zabbix-test.log
echo "---------------------------------" >> /tmp/zabbix-test.log
fi

