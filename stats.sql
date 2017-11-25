-------------------------------------------------------------------------------
-- This script will pull stats from the REPORTER database

-- To run this script, you must do the following:
--   (1) su to db2inst1

--   (2) db2 -td@ -vf stats.sql
--------------------------------------------------------------------------------
-- Connect:
CONNECT TO reporter USER db2inst1 @

--  SWATs for past 7 day
select count(*) SWATS, substr(Application,1,32) Application 
from REPORTER_STATUS 
where Manager = 'Page Ops Tool' and date(LastOccurrence) > CURRENT_DATE - 8 days
group by application @

-- Overall stats for past 7 days
select count(*) Events, OpsTeam 
from REPORTER_STATUS 
where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam > '' 
group by OpsTeam @

-- Detail for Storage
EXPORT TO storage.csv OF DEL MODIFIED BY NOCHARDEL 
select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence 
from REPORTER_STATUS 
where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'Storage' order by LastOccurrence DESC @

-- Detail for APM
EXPORT TO apm.csv OF DEL MODIFIED BY NOCHARDEL 
select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence 
from REPORTER_STATUS 
where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'APM' order by LastOccurrence DESC @

-- Detail of ICD
EXPORT TO icd.csv OF DEL MODIFIED BY NOCHARDEL 
select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence 
from REPORTER_STATUS 
where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'ICD' order by LastOccurrence DESC @

-- Detail of Network
EXPORT TO network.csv OF DEL MODIFIED BY NOCHARDEL 
select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence 
from REPORTER_STATUS 
where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'Network' order by LastOccurrence DESC @

-- Detail of Workload
EXPORT TO workload.csv OF DEL MODIFIED BY NOCHARDEL 
select Node, substr(AlertKey,1,32) AlertKey, substr(Application,1,32) Application, OriginalSeverity, substr(LastOccurrence, 1, 16) LastOccurrence 
from REPORTER_STATUS 
where OriginalSeverity > 3 and date(LastOccurrence) > CURRENT_DATE - 8 days and OpsTeam = 'Workload' order by LastOccurrence DESC @

-- SWATs for past 7 days
select count(*) SWATS, substr(Application,1,32) Application 
from REPORTER_STATUS 
where Manager = 'Page Ops Tool' and date(LastOccurrence) > CURRENT_DATE - 8 days
group by application @
