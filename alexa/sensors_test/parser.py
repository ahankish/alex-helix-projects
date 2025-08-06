# file for parsing the temperature output by time
# made to use with a script that runs lm-sensors and parses the json output
# made to run many time over a specific span of time 

#import pandas as pd
import json
import sys
import ROOT
ROOT.PyConfig.DisableRootLogon = True
ROOT.PyConfig.IgnoreCommandLineOptions = False

filename = sys.argv[1]
output_filename = sys.argv[2]
time = sys.srgv[3] # time of the event (in seconds)
sensors_out = {}

# parse the json file
with open(filename) as my_file:
  json_file = my_file.read()
  sensors_out = json.loads(json_file) 

# send the sensors output into a file 
def closeAtDestruct(name: str) -> None:
  outfile = ROOT.TFile.Open(name)
  # extract graph(s) and fill with the value(s) from the .json file
  output = sensors_out["nct6796-isa-0290"]["fan2"]["fan2_input"]
  #hist.Fill(output)

  fan_gr = outfile.FanGraph
  fan_gr.AddPoint(time, output) # time in sec. vs temp in fahrenheit

closeAtDestruct(output_filename)

### should i delete all the info in the .json file for the next run of sensors? 
### or should i append the new data and parse it that way?
### the data would need to be appended in the dictionary/json format
