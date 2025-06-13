#!/bin/bash

### from linuxconfig.org

# Log file path
LOG_FILE="/var/log/cpu_temp.log"

# Get CPU temperature
TEMP=$(sensors | grep 'Core 0' | awk '{print $3}')

# Get current date and time
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Write to log file
echo "$DATE - CPU Temperature: $TEMP" >> $LOG_FILE
