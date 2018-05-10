#!/bin/bash
python main.py $(date +'--day %d --month %m') >> check.log
python api_submit.py $(date +'--day %d --month %m') >> check.log
