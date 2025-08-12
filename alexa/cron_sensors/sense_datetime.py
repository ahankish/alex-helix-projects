#!/usr/bin/env python3
import subprocess
import pandas as pd
import json
import sys
from datetime import datetime

# inputs: sense_script.py [out-file name] [time step]
# Label input parameter args
out_fname = sys.argv[1] # String name of .csv file
#t_step = sys.argv[2] # How often this file is run 

# Runs the 'sensors' command and pipes the output to a file
subprocess.run(["touch", "tmp.json"])
#subprocess.run(["sensors", "-j", ">", "tmp.json"])
subprocess.Popen('sensors -j > tmp.json', shell=True)

# Parsing the 'sensors' output using the .json file
sensors_out = {}
with open("tmp.json") as my_file:
  #json_file = my_file.read()
  sensors_out = json.load(my_file) # Converts .json output into a dict

# Send the sensors output into a file 
# Managing the time entry
with open(out_fname, 'r') as file:
    is_empty = (file.read() == '')

date = datetime.now() # Current date
#print(date.strftime("%x"))
date_str = date.strftime("%x")
#print(date.strftime("%X"))
time_str = date.strftime("%X")

# Add up the time and convert to a float
time = 0.

if is_empty: 
    print("New File: Beginning log at Time = ", time)
    #time = float(time_str[0:1]*60) + float(time_str[3:4]) + float(time_str[6:7]/60) 
else: 
    # calculate the time based on the last time entry and the step value
    # or use datetime
    outfile = pd.read_csv(out_fname) # reading the outfile 
    first_time = outfile['Datetime'].loc[outfile.index[0]] # Format hr:min:sec
    #last_date = outfile['date'].loc[outfile.index[-1]] # Format month/day/year
    #if last_date == date_str:
    ftime_conv = (float(first_time[0:2]) * 60.0) + float(first_time[3:5]) + \
                 (float(first_time[6:]) / 60.0)
    new_time = (float(time_str[0:2]) * 60.0) + float(time_str[3:5]) + \
               (float(time_str[6:]) / 60.0)
    #print(60 * float(time_str[0:2]))
    #print(float(time_str[3:5]))
    #print(float(time_str[6:]) / 60)
    time = new_time - ftime_conv # How much time has elapsed since start in seconds
    #else: 
        #month_diff = str(int(date_str[0:1])-int(last_date[0:1]))
        #day_diff = str(int(date_str[3:4])-int(last_date[3:4]))
        #year_diff = str(int(date_str[6:7])-int(last_date[6:7]))

        # Convert the date difference into minutes
        #if (int(date_str[0:1]) < 8) and (int(date_str[0:1]) % 2 == 1): 
            #month_diff = (int(date_str[0:1])-int(last_date[0:1])) * 

# Extract the desired data from the .json file
output = sensors_out["nct6796-isa-0290"]["fan2"]["fan2_input"]
output1 = sensors_out["nct6796-isa-0290"]["SYSTIN"]["temp1_input"]
output2 = sensors_out["nct6796-isa-0290"]["CPUTIN"]["temp2_input"]

data_pt = {
        "Datetime": [time_str],
        "Time": [time],
        "Fan": [output],
        "Motherboard": [output1],
        "Motherboard CPU": [output2],
        }
# Turn the data into a Dataframe and append to the .csv log file
out_df = pd.DataFrame(data_pt)

if is_empty: 
    out_df.to_csv(out_fname, index=False, mode='a', header=True)
else:
    out_df.to_csv(out_fname, index=False, mode='a', header=False)
