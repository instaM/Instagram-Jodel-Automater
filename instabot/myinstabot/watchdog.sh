#!/bin/bash

path="/u/halle/bogusz/home_at/python/newinstabot/instabot/myinstabot/"
logfile=$path"log/logfile.log"
bot=$path"bot_run.py"
python $bot 
while [ 1 ]; do 
  # timestamp
  ts=`date +%T` 
  sleep 40
  #tail -30 $logfile | mail -s "Instabot Died at $ts" martin.bogusz@gmail.com 
  python $bot 
 
done
