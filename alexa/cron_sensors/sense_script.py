import subprocess
import pandas as pd
import json
import sys
#import numpy as np

# inputs: sense_script.py [out-file name] [time step]
# Label input parameter args
out_fname = sys.argv[1] # String name of .csv file
t_step = sys.argv[2] # How often this file is run 

# Runs the 'sensors' command and pipes the output to a file
subprocess.run(["touch", "tmp.json"])
subprocess.run(["sensors", "-j", ">", "tmp.json"])

# Parsing the 'sensors' output using the .json file
sensors_out = {}
with open("tmp.json") as my_file:
  #json_file = my_file.read()
  sensors_out = json.load(my_file) # Converts .json output into a dict

# Send the sensors output into a file 
# Managing the time entry
outfile = pd.read_csv(out_fname) # reading the outfile if it exists yet
time = 0
if outfile.empty(): 
    print("New File: Beginning log at Time = ", time)
else: 
    # calculate the time based on the last time entry and the step value
    # or use datetime
    last_time = outfile['Time'].loc[outfile.index[-1]]
    time = last_time + t_step

# Extract the desired data from the .json file
output = sensors_out["nct6796-isa-0290"]["fan2"]["fan2_input"]
output1 = sensors_out["nct6796-isa-0290"]["SYSTIN"]["temp1_input"]
output2 = output1 = sensors_out["nct6796-isa-0290"]["CPUTIN"]["temp2_input"]

data_pt = {
        "Time": time,
        "Fan": output,
        "Motherboard": output1,
        "Motherboard CPU": output2,
        }
# Turn the data into a Dataframe and append to the .csv log file
out_df = pd.DataFrame(data_pt)
if outfile.empty(): 
    out_df.to_csv(out_fname, index=False, mode='a', header=True)
else:
    out_df.to_csv(out_fname, index=False, mode='a', header=False)
