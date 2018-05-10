#!/bin/bash
python3 main.py $(date +'--day %d --month %m') >> check.log
python3 api_submit.py $(date +'--day %d --month %m') >> check.log
