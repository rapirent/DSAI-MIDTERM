#!/bin/bash
/usr/bin/python3 ~/DSAI-MIDTERM/main.py $(date +'--day %d --month %m') >> check.log
/usr/bin/python3 ~/DSAI-MIDTERM/api_submit.py $(date +'--day %d --month %m') >> check.log
/usr/bin/python3 ~/DSAI-MIDTERM/lastyear_submit.py >> check.log
