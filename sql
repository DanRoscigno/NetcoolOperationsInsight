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
