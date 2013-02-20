#!/usr/bin/perl -w

# $Revision: 1.1 $
# $Source: /usr/local/cvsroot/boxes/scripts/brave/ban-hackers.pl,v $
# %Location: /usr/local/sbin/
# %Servers:  brave

# script to take ip# hit by rules in apache mod_security
# and feed them to iptables to ban access to port 80 (http)


# BAN-HACKERS.PL written by Stanislaw Polak
# http://www.icsr.agh.edu.pl/~polak/
# 30 Nov 2006
#
# Copyright (c) 2006 Stanislaw Polak
# Unpublished work.
# Permission granted to use and modify this script so long as the
# copyright above is maintained, modifications are documented, and
# credit is given for any use of the script.
#
# For more information, see:
# http://www.icsr.agh.edu.pl/~polak/skrypty/ban-hackers.var    
#
#Version 1.03 (7 Apr 2008) 
#            Some modifications made by Dan MacNeil
#Version 1.02 (24 Jan 2007)
#	Locking was added	
#Version 1.01 (27 Dec 2006)
#		Problems with deleting a few the same rules has been fixed
#Version 1.0 (30 Nov 2006)
#             The first public version

# ASL: reload check
#if ( -e "/var/ossec/var/ossec.reload" ) {
#  exit;
#}


use DBI;
use strict;
use Fcntl qw (:flock);


my($ip,$dbh,$standard_period,$nonstandard_period,$max_elements,%whitelist,$dbname,$timestamp,$rule);

my $current_date=`/bin/date`;
chop $current_date;

######################################################################################################
# $standard_period    | elements which were added $standard_period seconds ago or ealier can be purged
######################################################################################################
# $max_elements       | when number of elements in the database exceedes $max_elements, elements
# $nonstandard_period | which were added $nonstandard_period seconds ago or ealier can be purged
######################################################################################################

# %whitelist          | hosts listed in %whitelist are never added to the database
######################################################################################################
# $dbname             | data are stored in the "$dbname" database
######################################################################################################
#$standard_period=5*24*60*60;  #120 hours
$standard_period=6*60*60;  #24 hours
$nonstandard_period=6*60*60; #24 hours
$max_elements=2000; 
%whitelist=(
	    "127.0.0.1"=>0,
	    "0.0.0.0"=>0
	    );
$dbname="/var/ossec/var/blocklist.sqlite";
############## open lock file ##############
my $lock_file = '/var/ossec/var/blocklist.lock'; 
open LOCKFILE, "<$lock_file"  or open LOCKFILE, ">>$lock_file" or warn "Cannot open $lock_file";
######################################################################################################

#$ip=$ENV{HTTP_X_FORWARDED_FOR};
$ip=$ENV{REMOTE_ADDR};


$dbh=&open_db;
#is script executed without arguments
if($#ARGV==-1 && $ip) { #add actual IP to the database
  # the script you execute must write something (anything) to stdout. 
  # If it doesn't ModSecurity will assume execution didn't work
  # If you write something to stdout cron will email it to you
  # so don't do that if running from cron and not ModSecurity
  print "\t.\n"; 

    # if connection was via proxy, address contains a list of client's IP
    # and proxies' IP - hacker's IP will be IP of last proxy
    my @ips=split(',',$ip); #the above addresses (elements of the list) are separated by "," 
    $ip=$ips[$#ips]; #hacker's IP is the last IP from the list 
    $ip =~s/^ *//;#Remove leading spaces:
    flock(LOCKFILE, LOCK_EX);
    if( !exists $whitelist{$ip} && !hacker_exists($dbh,$ip)){    #check if actual IP exists on the whitelist or in the database
	&add_hacker_db($dbh,$ip,time); #add hacker's IP if it doesn't exists yet
    }
    flock(LOCKFILE, LOCK_UN);
}

# Executed with the "add" argument (OSSEC)
elsif($ARGV[0] eq "add"){      #add the content of a database to iptables
  #$user=$ARGV[1];
  $ip=$ARGV[2];
  $timestamp=$ARGV[3];
  $rule=$ARGV[4];

  # Add to DB
  flock(LOCKFILE, LOCK_EX);
  if( !exists $whitelist{$ip} && !hacker_exists($dbh,$ip)){    #check if actual IP exists on the whitelist or in the database
    &add_hacker_db($dbh,$ip,$timestamp,$rule); #add hacker's IP if it doesn't exists yet
  }
  flock(LOCKFILE, LOCK_UN);

  # Shun 
  flock(LOCKFILE, LOCK_EX);
  &add_hacker_iptables($dbh);
  flock(LOCKFILE, LOCK_UN);

}
elsif($ARGV[0] eq "delete"){      #add the content of a database to iptables
    $ip=$ARGV[2];
    flock(LOCKFILE, LOCK_EX);
    &delete($dbh,$ip);
    flock(LOCKFILE, LOCK_UN);

}


#when script is executed with the "purge" argument
elsif($#ARGV==0 && $ARGV[0] eq "purge"){    #purge the content of the database
    flock(LOCKFILE, LOCK_EX);
    &purge($dbh);
    flock(LOCKFILE, LOCK_UN);
}
#when script is executed with the "load" argument
elsif($#ARGV==0 && $ARGV[0] eq "load"){      #add the content of a database to iptables
    flock(LOCKFILE, LOCK_EX);
    &add_hacker_iptables($dbh);
    flock(LOCKFILE, LOCK_UN);
}
#when script is executed with the "list" argument
elsif($#ARGV==0 && $ARGV[0] eq "list"){     #list the content of the database
    flock(LOCKFILE, LOCK_SH);
    my $query = qq{select * from hackers};
    my $sth= $dbh->prepare($query);
    $sth->execute;
    print "IP        \tTimestamp\tRule \n",'-' x 40,"\n";
    while (my (@data) = $sth->fetchrow_array) {
	my $time = localtime($data[1]);
        print "$data[0]\t $time\t $data[2]\n";
    }
    flock(LOCKFILE, LOCK_UN);
}
$dbh->disconnect;
close LOCKFILE or die "Cannot close $lock_file";
###############################################################################
###############################################################################
# opens a database and creates the "hackers" table  if it wasn't created ealier
sub open_db{
    my $dbh = DBI->connect("dbi:SQLite:dbname=$dbname","","") or die "Database connection not made: $DBI::errstr";
    if (! table_exists( $dbh, "hackers")) { #if the "hackers" table doesn't exists
	my $create_query = qq{     
	    create table hackers (
				  ip text unique,
				  time text not null,
				  rule integer
				  )
	    };
        $dbh->do( $create_query );          #create it
    }
    return $dbh;   #return a handler to the database
}

###############################################################################
# add the IP and time stamp to the "hackers" database
sub add_hacker_db{
    my $dbh= shift;
    my $ip = shift;
    my $time = shift;
    my $rule = shift;

    my @fields = (qw(ip time rule));
    my $fieldlist = join ", ", @fields;
    my $field_placeholders = join ", ", map {'?'} @fields;
    my $insert_query = qq{
        INSERT INTO hackers ( $fieldlist )
	    VALUES ( $field_placeholders )};
    my $sth= $dbh->prepare( $insert_query );
    $sth->execute($ip,$time,$rule);
}

###############################################################################
# add IPs stored in the database to the iptables
sub add_hacker_iptables{
    my $query = qq{select ip from hackers};
    my $sth= $dbh->prepare($query);
    $sth->execute;
	my $status;

    $status=system("/sbin/iptables  -L ASL-ACTIVE-RESPONSE | grep DROP > /dev/null 2>&1");

	if ($status != 0) {
		system("/sbin/iptables -N ASL-ACTIVE-RESPONSE >/dev/null");
                #system("/sbin/iptables -A ASL-ACTIVE-RESPONSE -m limit --limit 1/minute -j LOG  --log-level info --log-prefix 'ASL Active Response '");
		system("/sbin/iptables -A ASL-ACTIVE-RESPONSE -j DROP");
	}

	

    my @current_rules=`/sbin/iptables -L -n`;
    while (my ($ip) = $sth->fetchrow_array) {
	# null check
	next if ($ip == "");
	# don't create duplicate iptable rule
	next if scalar grep {/$ip/} @current_rules;

	# ASL
        my $cmd ="/sbin/iptables -I INPUT 1 -s $ip -j ASL-ACTIVE-RESPONSE";


	(system($cmd)==0) 
		or warn "returned failure: $cmd";

	# log the event
        system ("echo \"$current_date  asl-shun.pl add - $ip $timestamp $rule\" >> /var/ossec/logs/active-responses.log ");
    }

	
}
###############################################################################
#check if the "ip" of hacker exists in database
sub hacker_exists{
    my $dbh = shift;
    my $ip = shift;
    my $query = qq{select * from hackers where ip='$ip'};
    my $sth= $dbh->prepare($query);
    $sth->execute;
    my($result) = $sth->fetchrow_array;
    if($result){
	return length($result);
    }
    else {
	return 0;
    }
}
###############################################################################
# remove IP 
sub delete{
    my $dbh= shift;
    my $ip = shift;
    my $query = qq{select ip from hackers where ip='$ip'};

    my $sth= $dbh->prepare($query);
    $sth->execute;

    my @ips =();
    while (my ($ip) = $sth->fetchrow_array) {
        push @ips, $ip;
    }
    foreach $ip (@ips){ #remove "old" element from the database and from iptables
	#ASL
	my $cmd="/sbin/iptables -D INPUT -s $ip -j ASL-ACTIVE-RESPONSE 2>/dev/null";
	my $count;
	
	while (system($cmd)==0) {
		$count++;
	}

	$dbh->do(qq{
	    delete from hackers
		where ip='$ip'
	    } ) or die $dbh->errstr;
    }

	# Not working for some reason
    #system ("echo \"$current_date  asl-shun.pl delete - $ip $timestamp $rule\" >> /var/ossec/logs/active-responses.log ");
    system ("echo \"$current_date  asl-shun.pl delete - $ip\" >> /var/ossec/logs/active-responses.log ");

}

###############################################################################
# remove hachers IP after selected time
sub purge{
    my $dbh= shift;
    my($time)=time;
    #my(@rules)=(); #it contains all the rules from 'iptables'
    if($max_elements == 0 && $standard_period == 0){return;}
    
    #if there is less than $max_elements in the database
    if(count_hackers($dbh) <= $max_elements && $standard_period > 0){
	$time -= $standard_period;  #remove elements which are older than standard period
    }
    elsif($max_elements > 0) {
	$time -= $nonstandard_period; #else remove elements which are older than non-standard period
    }
    my $query = qq{select ip from hackers where time <= $time};
    my $sth= $dbh->prepare($query);
    $sth->execute;
    my @ips =();
    while (my ($ip) = $sth->fetchrow_array) {
        push @ips, $ip;
    }
    foreach $ip (@ips){ #remove "old" element from the database and from iptables
	#ASL
	my $cmd="/sbin/iptables -D INPUT -s $ip -j ASL-ACTIVE-RESPONSE";
	(system($cmd)==0) 
		or warn "returned failure: $cmd";

	$dbh->do(qq{
	    delete from hackers
		where ip='$ip'
	    } ) or die $dbh->errstr;
    }
}
###############################################################################
#check if  the table  exists in the data base
# source: http://gmax.oltrelinux.com/dbirecipes.html
sub table_exists {
    my $db = shift;
    my $table = shift;
    my @tables = $db->tables('','','','TABLE');
    if (@tables) {
	for (@tables) {
	    next unless $_;
	    return 1 if $_ eq $table
            }
    }
    else {
	eval {
	    local $db->{PrintError} = 0;
	    local $db->{RaiseError} = 1;
	    $db->do(qq{SELECT * FROM $table WHERE 1 = 0 });
	};
	return 1 unless $@;
    }
    return 0;
}
###############################################################################
# count the number of elements in the hackers table
sub count_hackers{
    my $dbh= shift;
    my $query=qq{SELECT COUNT(*) FROM hackers};
    my $sth= $dbh->prepare($query);
    $sth->execute;
    my ($count) = $sth->fetchrow_array; 
    return $count; 
}
