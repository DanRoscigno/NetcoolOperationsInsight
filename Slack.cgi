#!/opt/IBM/netcool/python27/bin/python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import time

print "Content-type: text/html"
print

print """
<html>

<head><title>Netcool to Slack</title></head>

<body>

  <h3> Netcool to Slack </h3>
All of the fields except for the <i>text that you want sent along</i>
should be pre-populated.  You can change all of the data other than
the Application.<br><br>

NOTE: If an event has a non-standard application name, the tool will
fail.  Please let me know if the tool fails and I will try to find out
why the application is not set correcty.<br><br>

Plese select the type of Slack message you would like to send, type in
your text, and push the <i>Send to Slack</i> button.<br><br>
"""

import os, sys
keys = os.environ.keys()
keys.sort()
#for k in keys:
    #print "%s\t%s" % (cgi.escape(k), cgi.escape(os.environ[k]))

# Extract the information we need from the os.environ() key value pairs.
# The fields passed in from Netcool (Node, Summary, etc., are in
# the QUERY_STRING, which looks like this:
# QUERY_STRING	datasource=OMNIBUS&$selected_rows.NodeAlias=foo-demo&$selected_rows.AlertKey=CSI_ISMBadWebSiteFatal&$selected_rows.application=NC&$selected_rows.Severity=5&$selected_rows.ITMDisplayItem=nc:foo-demo/Unity&CONVERSION.$selected_rows.Severity=Critical&$selected_rows.Summary=nc:foo-demo/Unity&$selected_rows.Node=foo-demo

alert_string = os.environ['QUERY_STRING'];

"""
Given an alert_string like so:
  datasource=OMNIBUS&$selected_rows.NodeAlias=foo-demo&$selected_rows.AlertKey=CSI_ISMBadWebSiteFatal
1) split the string into "<key>=<value>" chunks: s.split('&')
2) split each chunk into "<key> ", " <value>" pairs: item.split('=')
"""

alert_kvpairs = dict(item.split('=') for item in alert_string.split('&'))

"""
This gives me these keys:
    Key                              Description
 $selected_rows.AlertKey             AlertKey
 $selected_rows.NodeAlias            IP Address
 $selected_rows.Summary	             Summary
 $selected_rows.ITMDisplayItem	     Alternate Summary
 $selected_rows.application          Ops group (lookup for slack channel
 CONVERSION.$selected_rows.Severity  Severity String
 $selected_rows.Node                 Hostname
 $selected_rows.LastOccurrence       Time of most recent alert
"""

summary        = alert_kvpairs['$selected_rows.Summary']
itmdisplayitem = alert_kvpairs['$selected_rows.ITMDisplayItem']
if len(summary) == 0:
    summary = itmdisplayitem

node           = alert_kvpairs['$selected_rows.Node']
alertkey       = alert_kvpairs['$selected_rows.AlertKey']
nodealias      = alert_kvpairs['$selected_rows.NodeAlias']
severity       = alert_kvpairs['CONVERSION.$selected_rows.Severity']
application    = alert_kvpairs['$selected_rows.application']
#lastoccurrence = alert_kvpairs['$selected_rows.LastOccurrence']
lastoccurrence = time.strftime('%Y-%m-%d %H:%M', time.gmtime(float(alert_kvpairs['$selected_rows.LastOccurrence'])))


print '<form method="post" action="AlertOpsViaSlack.cgi">'

"""
print '<fieldset>'
print '<input type="radio" name="notification_type" value="nonurgent" required>   Non-urgent notification <br>'
print '<input type="radio" name="notification_type" value="tech_bridge" required> Tech Bridge             <br>'
print '<input type="radio" name="notification_type" value="swat_open" required>   SWAT Open               <br>'
print '<input type="radio" name="notification_type" value="swat_close" required>  SWAT Close              '
print '</fieldset>'
print '<br>'
"""
print '<fieldset>'
print '<legend>Text you want sent along with event content (why are you sending this to slack?)</legend>'
print '<input type="text" name="SRE_text" size="100" required>'
print '</fieldset>'
print '<br>'

print '<fieldset>'
print '<legend>Summary</legend>'
print '<input type="text" name="alert_summary" size="100" value="%s" required>' % summary
print '<br>'

print '<br>'
print '<legend>Alert Key</legend>'
print '<input type="text" name="alert_alertkey" size="100" value="%s">' % alertkey
print '</fieldset>'
print '<br>'

print '<fieldset>'
print '<legend>Node</legend>'
print '<input type="text" name="alert_node" size="100" value="%s">' % node
#print '</fieldset>'

print '<br>'
print '<br>'
print '<legend>Node Alias</legend>'
print '<input type="text" name="alert_nodealias" size="100" value="%s">' % nodealias
print '</fieldset>'
print '<br>'

print '<fieldset>'
print '<legend>Application (Read Only)</legend>'
print '<input type="text" name="alert_application" size="100" value="%s" readonly>' % application
print '</fieldset>'
print '<br>'

print '<fieldset>'
print '<legend>Last Occurrence (in GMT)</legend>'
print '<input type="text" name="alert_lastoccurrence" size="100" value="%s">' % lastoccurrence
print '</fieldset>'
print '<br>'

print '<fieldset>'
print '<legend>Severity</legend>'
print '<input type="text" name="alert_severity" size="100" value="%s">' % severity
print '</fieldset>'
print '<br>'


print """
  <input type="submit" value="Send to Slack">
  </form>
  <pre>
  </pre>
</body>

</html>
"""
# % cgi.escape(message)
