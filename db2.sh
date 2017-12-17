#!/bin/sh
source /home/db2inst1/sqllib/db2profile
db2 -x "CONNECT TO reporter USER db2inst1 USING C\@tf00d" >/dev/null 2>&1
db2 -x "SELECT \
         '<TR>',\
               '<TD>', Application, '</TD>', \
               '<TD>', substr(FirstOccurrence, 1, 16) FirstOccurrence, '</TD>', \
               '<TD>', substr(LastOccurrence, 1, 16) LastOccurrence, '</TD>', \
               '<TD>', REPORTER_NAMES.NAME, '</TD>', \
               '<TD>', Node, '</TD>', \
               '<TD>', AlertKey, '</TD>', \
         '</TR>', \
         '<TR>', \
               '<TD COLSPAN="5">Summary: ', Summary, '</TD>', \
         '</TR>', \
         '<TR>', \
               '<TD COLSPAN="5">&nbsp;</TD>', \
         '</TR>' \
       FROM REPORTER_STATUS \
       INNER JOIN REPORTER_NAMES ON REPORTER_NAMES.OWNERUID = REPORTER_STATUS.OWNERUID \
       WHERE  Node = '$1' \
       ORDER BY  LastOccurrence DESC \
       FETCH  FIRST 50 ROWS ONLY" 
