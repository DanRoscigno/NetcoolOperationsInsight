#!/opt/IBM/netcool/python27/bin/python
import cgi
import cgitb
cgitb.enable()
print "Content-type: text/html"
print

print """
<html>

<head><title>Netcool to Slack</title></head>

<body>

  <h3> Netcool to Slack </h3>
<br><br>
  <pre>
"""

import json
import requests

"""
Put your webhook url that looks like:
   https://hooks.slack.com/services/TXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXXXXXXXXX'
and the slack channel name for each ops team in a file named
webhooktoken.ini in this format:

[APPNAME1]
token: https://hooks.slack.com/services/TXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXXXXXXXXX
channel: app1-ops-events

[APPNAME2]
token: https://hooks.slack.com/services/TXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXXXXXXXXX
channel: app2-ops-events
"""

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("/opt/IBM/netcool/gui/omnibus_webgui/etc/cgi-bin/webhooktoken.ini")

import os, sys
from cgi import escape

keys = os.environ.keys()

import urlparse
alert_info = {}
alert_info = dict(urlparse.parse_qsl(os.environ['QUERY_STRING']))
keys = alert_info.keys()
keys.sort()
for k in keys:
    print "%s\t\t%s" % (cgi.escape(k), cgi.escape(alert_info[k]))

print "%s\t\t%s" % ('WEBTOP_USER', os.environ['WEBTOP_USER'])

print """
  </pre>
"""
"""
This gives me these keys:
    Key				          Description
  SRE_text    		      Freeform text typed in the Slack form
  alert_alertkey		    AlertKey
  alert_application		  Ops group (lookup for slack channel)
  alert_lastoccurrence  Most recent time (GMT) this occurred
  alert_node            Hostname
  alert_nodealias       Alternate (hopefully IP) Hostname
  alert_summary         Summary or ITMDisplayItem from netcool
  notification_type     Type of Slack request
  WEBTOP_USER           Username in Netcool
"""

sre_text       = alert_info['SRE_text']
summary        = alert_info['alert_summary']
node           = alert_info['alert_node']
alertkey       = alert_info['alert_alertkey']
nodealias      = alert_info['alert_nodealias']
severity       = alert_info['alert_severity']
application    = alert_info['alert_application']
user           = os.environ['WEBTOP_USER']

if severity == 'Critical':
	color = 'danger'
else:
	color = 'warning'
# Up top we read the config, now we will lookup the channel and token
channel = Config.get(application, 'channel')
token   = Config.get(application, 'token')

slack_data = {
    "channel": "%s" % channel,
    # This next line subs the var user in for the SRE's name, and we got that name from os.environ['WEBTOP_USER']
    "text": "Sent by SRE %s" % user,
    "attachments": [
        {
            "fallback": "Summary: %s, Node: %s, AlertKey: %s, NodeAlias: %s, Severity: Critical." % (summary, node, alertkey, nodealias),
            "title": "Alert from SRE team",
            "color": "%s" % color,
            "fields": [
                {
                    "short": "false",
                    "value": "%s" % sre_text,
                    "title": "Note"
                },
                {
                    "short": "false",
                    "value": "%s" % summary,
                    "title": "Summary"
                },
                {
                    "short": "false",
                    "value": "%s" % node,
                    "title": "Node"
                },
                {
                    "short": "false",
                    "value": "%s" % alertkey,
                    "title": "AlertKey"
                },
                {
                    "short": "true",
                    "value": "%s" % nodealias,
                    "title": "NodeAlias"
                },
                {
                    "short": "true",
                    "value": "%s" % severity,
                    "title": "Severity"
                }
            ]
        }
    ]
}

slackResponse = requests.post(
    token, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)

if slackResponse.status_code != 200:
    raise ValueError(
        'There was an error (%s) during posting the message to slack, the response is:\n%s'
        % (slackResponse.status_code, slackResponse.text)
    )
else:
    print "Successfully posted to %s" % channel

print """


  </pre>
</body>

</html>
"""

#print json.dumps(slack_data, sort_keys=False, indent=4, separators=(',', ': '))
