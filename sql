# Use OriginalSeverity when selecting against Reporter_Status
#
#  Get the top event producers by AlertKey
select count(*) Count, substr(AlertKey, 1, 40) AlertKey from reporter_status where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days group by AlertKey order by Count desc FETCH FIRST 5 ROWS ONLY

#  Get the top event producers by Application and AlertKey
select count(*) Count, substr(Application, 1, 36) Application, substr(AlertKey, 1, 40) AlertKey from reporter_status where OriginalSeverity > 3 and Class > 0 and date(LastOccurrence) > CURRENT_DATE - 8 days and Application > '' group by Application, AlertKey order by Count desc FETCH FIRST 5 ROWS ONLY

#  Get the top event producers by Application and AlertKey and Manager
select count(*) Count, substr(Application, 1, 36) Application, substr(AlertKey, 1, 40) AlertKey, substr(Manager, 1, 16) Manager from reporter_status where OriginalSeverity > 3 and Class > 0 and date(LastOccurrence) > CURRENT_DATE - 8 days and Application > '' group by Application, AlertKey, Manager order by Count desc FETCH FIRST 15 ROWS ONLY

#  Check for the most recent event for each probe / tool:
select substr(Manager, 1, 40) Manager, substr(to_char(max(LastOccurrence), 'YYYY-MM-DD HH24:MI:SS'), 1, 22) Last from reporter_status group by Manager order by Last desc

# Find the strings used as "Application"
select Count(*), Application from reporter_status where Class > 0 group by Application

select AlertKey, Application, OriginalSeverity, substr(to_char(LastOccurrence), 'YYYY-MM-DD HH24:MI:SS', 1, 22) from REPORTER_STATUS where OriginalSeverity > 3  and Application in ('TWS', 'WA')

select substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3  and Application in ('TWS', 'WA') order by LastOccurrence DESC

substr(to_char(max(LastOccurrence), 'YYYY-MM-DD HH24:MI:SS')

select substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3 and Application in ('TPC', 'Storage Insights Devops', 'Storage', 'StorageAnalytics') order by LastOccurrence DESC

EXPORT TO result.csv OF DEL MODIFIED BY NOCHARDEL select substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3 and Application in ('TPC', 'Storage Insights Devops', 'Storage', 'StorageAnalytics') order by LastOccurrence DESC

EXPORT TO result.csv OF DEL MODIFIED BY NOCHARDEL select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3 and Application in ('TPC', 'Storage', 'StorageAnalytics') order by LastOccurrence DESC

EXPORT TO result.csv OF DEL MODIFIED BY NOCHARDEL SELECT col1, col2, coln FROM testtable;

select distinct substr(Application,1,52) Application from REPORTER_STATUS ORDER BY Application ASC

select Application, AlertKey, OpsTeam, Service from REPORTER_STATUS where Service > ''

select distinct substr(Application,1,64) from REPORTER_STATUS


Workload:
select min(lastoccurrence) Start, max(LastOccurrence) End, count(*) from reporter_status where OriginalSeverity > 3 and Application in ('WA', 'TWS')

Storage:
select min(lastoccurrence) Start, max(LastOccurrence) End, count(*) from reporter_status where OriginalSeverity > 3 and Application in ('TPC', 'StorageAnalytics')

Control Desk:
select min(lastoccurrence) Start, max(LastOccurrence) End, count(*) from reporter_status where OriginalSeverity > 3 and Application in ('SCCD-JLL-TUNNEL2 - MONITORED', 'SCCD-JLL-TUNNEL1 - MONITORED', 'SCCD', 'FULLSAIL -MONITORED', 'JL LDAP to AD - MONITORED', 'AeroMexico -- AeroMex SCCD MONITORED', 'Bendigo - MONITORED', 'Bendigo / SCCD - MONITORED')

APM:
select min(lastoccurrence) Start, max(LastOccurrence) End, count(*) from reporter_status where OriginalSeverity > 3 and Application in ('APM', 'FEDERAL_APM')

Predict:
select min(lastoccurrence) Start, max(LastOccurrence) End, count(*) from reporter_status where OriginalSeverity > 3 and Application in ('PI', 'PredictivInsight')

# Overall stats for past 7 days
select count(*) Events, OpsTeam from REPORTER_STATUS where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam > '' group by OpsTeam

# Detail for Storage
EXPORT TO storage.csv OF DEL MODIFIED BY NOCHARDEL select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'Storage' order by LastOccurrence DESC

# Detail for APM
EXPORT TO apm.csv OF DEL MODIFIED BY NOCHARDEL select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'APM' order by LastOccurrence DESC

# Detail of ICD
EXPORT TO icd.csv OF DEL MODIFIED BY NOCHARDEL select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'ICD' order by LastOccurrence DESC

# Detail of Network
EXPORT TO network.csv OF DEL MODIFIED BY NOCHARDEL select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'Network' order by LastOccurrence DESC

# Detail of Workload
EXPORT TO workload.csv OF DEL MODIFIED BY NOCHARDEL select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence from REPORTER_STATUS where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'Workload' order by LastOccurrence DESC

# SWATs for past 7 days
select count(*) SWATS, substr(Application,1,32) Application from REPORTER_STATUS where Manager = 'Page Ops Tool' and date(LastOccurrence) > CURRENT_DATE - 8 days group by application
