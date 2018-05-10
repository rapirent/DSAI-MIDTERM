#!/bin/bash
/usr/bin/python3 main.py $(date +'--day %d --month %m') >> check.log
/usr/bin/python3 api_submit.py $(date +'--day %d --month %m') >> check.log
/usr/bin/python3 lastyear_submit.py >> check.log
