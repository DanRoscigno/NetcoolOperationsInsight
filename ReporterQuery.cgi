#!/usr/bin/perl
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
use CGI::Pretty;
use CGI;
use DBI;
#use DBD::DB2::Constants;
#use DBD::DB2;

# Get the input
$buffer = $ENV{'QUERY_STRING'};
@pairs = split(/&/, $buffer);

foreach $pair (@pairs)
{
    ($name, $value) = split(/=/, $pair);

    # Un-Webify plus signs and %-encoding
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

    $name =~ tr/+/ /;
    $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg; 
    
    $FORM{$name} = $value;
}

print "Content-type: text/html\n\n";
print <<__HTML__;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>History Lookup</TITLE>

<STYLE type="text/css">
h1.headerTool
{
	font-size: 30pt;
	font-style: italic;
	font-weight: bold;
	letter-spacing: -4px;
}

.headerReg, .headerTM
{
	font-size: 12pt;
	vertical-align: super;
}

.headerWebtop
{
	font-size: 28;
	font-weight: 500;
	letter-spacing: 0px;
}

body
{
	background-color: #000033;
	color: #ffffff;
	font-family: Arial, Verdana, sans-serif;
}

.systemMsg
{
	font-size: 14pt;
	font-weight: bold;
}
</STYLE>
</HEAD>
<BODY>

<h1 class="headerWebtop">Tivoli Netcool/OMNIbus Web GUI</h1>
<CENTER>
<HR HEIGHT="15" >
</CENTER>
__HTML__

$nodeName = "";

if (! $FORM{"\$selected_rows.Node"}) {
	print "<p class=\"systemMsg\">No Node Specified.</p></body></html>";
	die;
}
else {
	$nodeName = $FORM{"\$selected_rows.Node"};
	# Host names are limited to a subset of ASCII characters, so filter out the rest
	$nodeName =~ s/[^a-zA-Z0-9._\-]*//g;
	print "<p class=\"systemMsg\">History for host ".$nodeName."</p>\n";

# from 
	print " <TABLE BORDER=1 CELLPADDING=8> "; 
	print " <TR> "; 
	print " <TH>Application</TH> "; 
	print " <TH>First Occurrence</TH> "; 
	print " <TH>Last Occurrence</TH> "; 
	print " <TH>Owner</TH> "; 
	print " <TH>Node</TH> "; 
	print " <TH>AlertKey</TH> "; 
	print " </TR> "; 
}

open(DATABASEHANDLE,"/opt/IBM/netcool/DatabaseAccess/db2.sh ".$nodeName."|");
$old_fh = select(STDOUT);
$| = 1;
select($old_fh);

#print "<PRE>";
while(<DATABASEHANDLE>) {
	print;
}
#print "</PRE>";
	print "</TABLE>";
print "<CENTER><HR HEIGHT=\"15\" ></CENTER>";
print <<__HTML__;
<form action="">
<div align="center"><input type="button" value="Close Window" onClick="javascript:window.close();"></div>
</form>
</BODY>
</HTML>
__HTML__
