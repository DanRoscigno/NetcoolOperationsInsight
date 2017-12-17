#!/opt/IBM/netcool/python27/bin/python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import time

print "Content-type: text/html"
print

print """
<html>

<head><title>Create Slack Channel</title></head>

<body>

  <pre>
"""

import os, sys
keys = os.environ.keys()
keys.sort()
#for k in keys:
    #print "%s\t%s" % (cgi.escape(k), cgi.escape(os.environ[k]))

# Extract the information we need from the os.environ() key value pairs.
# The fields passed in from Netcool (Node, Summary, etc., are in
# the QUERY_STRING, which looks like this:
# export QUERY_STRING='datasource=OMNIBUS&$selected_rows.application=NC&$selected_rows.TTNumber=SRFAKE&$selected_rows.Identifier=ID12345&$selected_rows.LastOccurrence=1234567890'

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
 $selected_rows.TTNumber             The session number for this customer issue
 $selected_rows.Identifier           The unique identifier for the OMNIbus event so that we can update it
 $selected_rows.application          Ops group (lookup for slack channel
 $selected_rows.LastOccurrence       Time of most recent alert
"""

session        = alert_kvpairs['$selected_rows.TTNumber']
identifier     = alert_kvpairs['$selected_rows.Identifier']
application    = alert_kvpairs['$selected_rows.application']
lastoccurrence = alert_kvpairs['$selected_rows.LastOccurrence']

import requests
import json
import sys

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("/opt/IBM/netcool/gui/omnibus_webgui/etc/cgi-bin/AlertNotification.ini")

# Up top we read the config, now we will lookup the username and password for Alert Notification
token = Config.get('SLACKTEAM', 'token')
URI   = Config.get('SLACKTEAM', 'URI')

channel = 'sre-' + session + '-' + application

r = requests.post(URI, data={'token': token, 'name': channel})
r.raise_for_status()
if not r.ok:
    raise ValueError(
        'There was an http error (%s) during creating the channel, the response is:\n%s'
        % (r.status_code, r.text)
    )
    sys.exit(1)
else:
    print "http POST OK"
    resp_dict = json.loads(r.text)
    if not resp_dict['ok']:
        print 'The channel creation failed, the error message is:\n%s' % resp_dict['error']
    else:
        print 'Channel creation OK'
        print 'Channel name: %s' % resp_dict["channel"]["name_normalized"]
        print 'Channel ID: %s' % resp_dict["channel"]["id"]
   

print """
  </pre>
  <br>
  <form action="">
    <div align="center"><input type="button" value="Close Window" onClick="javascript:window.close();"></div>
  </form>
</body>

</html>
"""
# % cgi.escape(message)
